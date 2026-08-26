"""
Semaine 4 — Jour 2
Lab : Abstraction Agent

Objectif :
Construire une abstraction Agent testable, indépendante d'un fournisseur LLM.

Exécution :
    python agent_abstraction.py
    python test_agent_abstraction.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Protocol
import json
import re
import time


VALID_STATUSES = {"completed", "blocked", "failed"}


@dataclass(frozen=True)
class TraceEvent:
    """Événement de trace simple et sérialisable."""

    step: str
    message: str
    timestamp_ms: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step,
            "message": self.message,
            "timestamp_ms": self.timestamp_ms,
        }


@dataclass
class RunContext:
    """Entrée standard d'un agent."""

    user_input: str
    session_id: str
    user_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_input": self.user_input,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "metadata": dict(self.metadata),
        }


@dataclass
class ModelRequest:
    """Requête générique envoyée à un ModelClient."""

    model: str
    messages: List[Dict[str, str]]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelResponse:
    """Réponse normalisée d'un ModelClient."""

    text: str
    usage: Dict[str, int] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


class ModelClient(Protocol):
    """Interface minimale que tout client modèle doit respecter."""

    def complete(self, request: ModelRequest) -> ModelResponse:
        ...


@dataclass
class AgentResult:
    """Sortie standard d'un agent."""

    agent_name: str
    output: str
    status: str
    usage: Dict[str, int]
    trace: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.status not in VALID_STATUSES:
            raise ValueError(f"Invalid status: {self.status}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "output": self.output,
            "status": self.status,
            "usage": dict(self.usage),
            "trace": list(self.trace),
            "metadata": dict(self.metadata),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class EchoModelClient:
    """
    Faux modèle déterministe.

    Il permet de tester l'agent sans appel réseau.
    """

    def __init__(self, canned_response: str | None = None) -> None:
        self.canned_response = canned_response
        self.calls: List[ModelRequest] = []

    def complete(self, request: ModelRequest) -> ModelResponse:
        self.calls.append(request)
        if self.canned_response is not None:
            text = self.canned_response
        else:
            user_message = next(
                (m["content"] for m in reversed(request.messages) if m["role"] == "user"),
                "",
            )
            text = f"Réponse simulée pour: {user_message}"
        input_chars = sum(len(m["content"]) for m in request.messages)
        return ModelResponse(
            text=text,
            usage={"input_chars": input_chars, "output_chars": len(text)},
            raw={"provider": "echo", "model": request.model},
        )


@dataclass
class Agent:
    """
    Abstraction Agent du mini-framework.

    Cette classe ne dépend d'aucun SDK fournisseur.
    """

    name: str
    instructions: str
    model_client: ModelClient
    model: str = "fake-model"
    max_input_chars: int = 4000
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._validate_definition()

    def _now_ms(self) -> int:
        return int(time.time() * 1000)

    def _event(self, step: str, message: str) -> TraceEvent:
        return TraceEvent(step=step, message=message, timestamp_ms=self._now_ms())

    def _validate_definition(self) -> None:
        if not re.match(r"^[a-z][a-z0-9_]{2,63}$", self.name):
            raise ValueError(
                "Agent name must start with a lowercase letter and contain "
                "only lowercase letters, digits and underscores."
            )
        if not self.instructions or len(self.instructions.strip()) < 10:
            raise ValueError("Agent instructions must contain at least 10 characters.")
        if not self.model:
            raise ValueError("Agent model must not be empty.")
        if self.max_input_chars <= 0:
            raise ValueError("max_input_chars must be positive.")

    def _blocked_result(
        self,
        reason: str,
        context: RunContext,
        trace: List[TraceEvent],
    ) -> AgentResult:
        trace.append(self._event("blocked", reason))
        return AgentResult(
            agent_name=self.name,
            output="",
            status="blocked",
            usage={"input_chars": len(context.user_input), "output_chars": 0},
            trace=[event.to_dict() for event in trace],
            metadata={"reason": reason, **self.metadata},
        )

    def _apply_guardrails(
        self,
        context: RunContext,
        trace: List[TraceEvent],
    ) -> str | None:
        trace.append(self._event("guardrails", "Checking run context."))

        if not context.user_input or not context.user_input.strip():
            return "User input must not be empty."

        if len(context.user_input) > self.max_input_chars:
            return "User input exceeds max_input_chars."

        if "DROP TABLE" in context.user_input.upper():
            return "Unsafe database instruction blocked."

        return None

    def build_messages(self, context: RunContext) -> List[Dict[str, str]]:
        """Construit les messages de manière déterministe."""
        return [
            {
                "role": "system",
                "content": self.instructions.strip(),
            },
            {
                "role": "user",
                "content": context.user_input.strip(),
            },
        ]

    def run(self, context: RunContext) -> AgentResult:
        trace: List[TraceEvent] = [
            self._event("start", f"Agent {self.name} started.")
        ]

        violation = self._apply_guardrails(context, trace)
        if violation:
            return self._blocked_result(violation, context, trace)

        trace.append(self._event("prompt", "Building model request."))
        messages = self.build_messages(context)

        request = ModelRequest(
            model=self.model,
            messages=messages,
            metadata={
                "agent_name": self.name,
                "session_id": context.session_id,
                "user_id": context.user_id,
                **self.metadata,
                **context.metadata,
            },
        )

        try:
            trace.append(self._event("model_call", "Calling model client."))
            response = self.model_client.complete(request)
            trace.append(self._event("complete", "Agent completed successfully."))
            return AgentResult(
                agent_name=self.name,
                output=response.text,
                status="completed",
                usage=response.usage,
                trace=[event.to_dict() for event in trace],
                metadata={
                    "model": self.model,
                    "session_id": context.session_id,
                    "user_id": context.user_id,
                    **self.metadata,
                },
            )
        except Exception as exc:  # pragma: no cover - defensive path
            trace.append(self._event("failed", str(exc)))
            return AgentResult(
                agent_name=self.name,
                output="",
                status="failed",
                usage={"input_chars": len(context.user_input), "output_chars": 0},
                trace=[event.to_dict() for event in trace],
                metadata={"error": str(exc), **self.metadata},
            )


def demo() -> AgentResult:
    client = EchoModelClient(
        canned_response=(
            "Un agent est une unité d'exécution spécialisée. "
            "Dans un framework, il reçoit un contexte, appelle un modèle abstrait "
            "et retourne un résultat standardisé."
        )
    )
    agent = Agent(
        name="explainer",
        instructions="Explique les concepts AI Engineering avec un exemple concret.",
        model_client=client,
        model="fake-model",
        metadata={"course": "ai-engineering-bootcamp", "week": 4, "day": 2},
    )
    return agent.run(
        RunContext(
            user_input="Explique le rôle d'une abstraction Agent.",
            session_id="session-demo",
            user_id="learner-demo",
            metadata={"source": "lab"},
        )
    )


if __name__ == "__main__":
    print(demo().to_json())
