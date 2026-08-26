"""
Semaine 2 — Jour 6 — Agent Loop & planification.

Ce module implémente une boucle agentique déterministe.

Il ne dépend pas d'un LLM réel afin de rendre les tests reproductibles.
Dans une application de production, la policy déterministe pourrait être
remplacée ou augmentée par un modèle produisant des Structured Outputs.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
import json
import re
from typing import Any, Callable


@dataclass(frozen=True)
class PlanStep:
    """Étape intentionnelle du plan."""

    step_id: str
    description: str
    completed: bool = False


@dataclass(frozen=True)
class ToolAction:
    """Action concrète que la boucle veut exécuter."""

    tool_name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class Observation:
    """Résultat d'une action."""

    tool_name: str
    success: bool
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass
class AgentState:
    """État courant de résolution d'une tâche agentique."""

    goal: str
    user_message: str
    status: str = "running"
    iterations: int = 0
    max_iterations: int = 5
    order_id: str | None = None
    order_status: str | None = None
    eta: str | None = None
    final_answer: str | None = None
    plan: list[PlanStep] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)

    def to_json(self) -> str:
        """Sérialise l'état pour logging ou persistance courte durée."""

        return json.dumps(asdict(self), ensure_ascii=False, indent=2)

    def is_terminal(self) -> bool:
        """Indique si la boucle doit s'arrêter."""

        return self.status in {
            "completed",
            "waiting_for_user",
            "error",
            "max_iterations_reached",
        }


class ToolRegistry:
    """Registre des outils autorisés par l'application."""

    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., dict[str, Any]]] = {}

    def register(self, name: str, fn: Callable[..., dict[str, Any]]) -> None:
        if not name:
            raise ValueError("Tool name cannot be empty.")
        self._tools[name] = fn

    def has_tool(self, name: str) -> bool:
        return name in self._tools

    def execute(self, action: ToolAction) -> Observation:
        if action.tool_name not in self._tools:
            return Observation(
                tool_name=action.tool_name,
                success=False,
                error=f"Unknown tool: {action.tool_name}",
            )

        try:
            data = self._tools[action.tool_name](**action.arguments)
            return Observation(tool_name=action.tool_name, success=True, data=data)
        except Exception as exc:  # pragma: no cover - protection de production
            return Observation(
                tool_name=action.tool_name,
                success=False,
                error=str(exc),
            )


def extract_order_id(message: str) -> str | None:
    """Extrait un identifiant de commande au format A-100, B-245, etc."""

    match = re.search(r"\b[A-Z]-\d{3,}\b", message)
    return match.group(0) if match else None


def lookup_order(order_id: str) -> dict[str, Any]:
    """Outil simulé de récupération de commande."""

    fake_database = {
        "A-100": {
            "order_id": "A-100",
            "status": "delayed",
            "eta": "2026-09-02",
        },
        "B-245": {
            "order_id": "B-245",
            "status": "in_transit",
            "eta": "2026-08-28",
        },
    }

    if order_id not in fake_database:
        raise ValueError(f"Order {order_id} not found.")

    return fake_database[order_id]


def draft_support_reply(order_id: str, status: str, eta: str) -> dict[str, Any]:
    """Outil simulé de rédaction de réponse support."""

    if status == "delayed":
        answer = (
            f"Bonjour, votre commande {order_id} est actuellement retardée. "
            f"La livraison est estimée au {eta}. "
            "Nous sommes désolés pour ce délai."
        )
    else:
        answer = (
            f"Bonjour, votre commande {order_id} est actuellement en statut "
            f"{status}. La livraison est estimée au {eta}."
        )

    return {"final_answer": answer}


class AgentLoop:
    """Boucle agentique plan -> act -> observe -> update -> decide."""

    def __init__(self, registry: ToolRegistry, max_iterations: int = 5) -> None:
        if max_iterations < 1:
            raise ValueError("max_iterations must be >= 1.")
        self.registry = registry
        self.max_iterations = max_iterations

    def initialize_state(self, user_message: str) -> AgentState:
        state = AgentState(
            goal="Résoudre une demande support liée à une commande.",
            user_message=user_message,
            max_iterations=self.max_iterations,
            order_id=extract_order_id(user_message),
        )
        state.plan = self.create_plan(state)
        return state

    def create_plan(self, state: AgentState) -> list[PlanStep]:
        """Produit un plan initial ou un plan adapté aux informations connues."""

        if state.order_id is None:
            return [
                PlanStep("step_1", "Demander l'identifiant de commande au client."),
            ]

        return [
            PlanStep("step_1", "Consulter l'état de la commande."),
            PlanStep("step_2", "Rédiger une réponse support."),
            PlanStep("step_3", "Terminer avec une réponse finale contrôlée."),
        ]

    def choose_next_action(self, state: AgentState) -> ToolAction:
        """Politique déterministe de choix d'action."""

        if state.order_id is None:
            return ToolAction(
                "ask_clarification",
                {
                    "question": "Pouvez-vous me transmettre votre identifiant de commande ?"
                },
            )

        if state.order_status is None or state.eta is None:
            return ToolAction("lookup_order", {"order_id": state.order_id})

        if state.final_answer is None:
            return ToolAction(
                "draft_support_reply",
                {
                    "order_id": state.order_id,
                    "status": state.order_status,
                    "eta": state.eta,
                },
            )

        return ToolAction("finish", {})

    def reduce(self, state: AgentState, action: ToolAction, observation: Observation) -> None:
        """Met à jour l'état à partir d'une observation."""

        updated_fields: list[str] = []

        if action.tool_name == "ask_clarification":
            state.status = "waiting_for_user"
            state.final_answer = action.arguments["question"]
            updated_fields.extend(["status", "final_answer"])

        elif not observation.success:
            state.status = "error"
            updated_fields.append("status")

        elif action.tool_name == "lookup_order":
            state.order_status = observation.data["status"]
            state.eta = observation.data["eta"]
            updated_fields.extend(["order_status", "eta"])

        elif action.tool_name == "draft_support_reply":
            state.final_answer = observation.data["final_answer"]
            state.status = "completed"
            updated_fields.extend(["final_answer", "status"])

        elif action.tool_name == "finish":
            state.status = "completed"
            updated_fields.append("status")

        state.trace.append(
            {
                "iteration": state.iterations,
                "action": action.tool_name,
                "arguments": action.arguments,
                "success": observation.success,
                "error": observation.error,
                "updated_fields": updated_fields,
            }
        )

    def run(self, user_message: str) -> AgentState:
        state = self.initialize_state(user_message)

        while not state.is_terminal():
            if state.iterations >= state.max_iterations:
                state.status = "max_iterations_reached"
                state.trace.append(
                    {
                        "iteration": state.iterations,
                        "action": "stop",
                        "arguments": {},
                        "success": False,
                        "error": "Maximum iterations reached.",
                        "updated_fields": ["status"],
                    }
                )
                break

            state.iterations += 1
            action = self.choose_next_action(state)

            if action.tool_name in {"ask_clarification", "finish"}:
                observation = Observation(tool_name=action.tool_name, success=True)
            else:
                observation = self.registry.execute(action)

            self.reduce(state, action, observation)

        return state


def build_default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register("lookup_order", lookup_order)
    registry.register("draft_support_reply", draft_support_reply)
    return registry


def main() -> None:
    registry = build_default_registry()
    loop = AgentLoop(registry=registry, max_iterations=5)

    state = loop.run("Bonjour, ma commande A-100 est en retard. Pouvez-vous m'aider ?")

    print(state.to_json())
    print()
    print("Réponse finale:")
    print(state.final_answer)


if __name__ == "__main__":
    main()
