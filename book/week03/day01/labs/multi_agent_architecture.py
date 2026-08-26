"""
Semaine 3 — Jour 1
Lab : Simulation déterministe d'une architecture multi-agents.

Aucune dépendance externe.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
import json


class ArchitectureError(ValueError):
    """Erreur de configuration d'architecture multi-agents."""


class TaskStatus(str, Enum):
    NEEDS_CLARIFICATION = "needs_clarification"
    COMPLETED = "completed"
    REJECTED = "rejected"


@dataclass(frozen=True)
class Task:
    ticket_id: str
    message: str
    user_id: str = "anonymous"


@dataclass(frozen=True)
class AgentSpec:
    name: str
    role: str
    keywords: Tuple[str, ...]
    allowed_tools: Tuple[str, ...] = ()
    can_handoff: bool = False

    def matches(self, message: str) -> int:
        normalized = message.lower()
        return sum(1 for keyword in self.keywords if keyword.lower() in normalized)


@dataclass
class RoutingDecision:
    target_agent: Optional[str]
    confidence: float
    reason: str
    requires_clarification: bool = False

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


@dataclass
class AgentResult:
    agent: str
    answer: str
    status: TaskStatus
    risk_level: str = "low"
    requires_human_review: bool = False

    def to_dict(self) -> Dict[str, object]:
        data = asdict(self)
        data["status"] = self.status.value
        return data


@dataclass
class TraceEvent:
    step: int
    agent: str
    action: str
    status: str
    detail: str

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


@dataclass
class MultiAgentRun:
    task: Task
    routing: RoutingDecision
    result: Optional[AgentResult]
    reviewed: bool
    final_answer: str
    trace: List[TraceEvent] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(
            {
                "task": asdict(self.task),
                "routing": self.routing.to_dict(),
                "result": None if self.result is None else self.result.to_dict(),
                "reviewed": self.reviewed,
                "final_answer": self.final_answer,
                "trace": [event.to_dict() for event in self.trace],
            },
            ensure_ascii=False,
            indent=2,
        )


class MultiAgentArchitecture:
    """Architecture multi-agents déterministe et testable."""

    def __init__(
        self,
        agents: Sequence[AgentSpec],
        reviewer_name: str = "reviewer",
        ambiguity_threshold: float = 0.51,
    ) -> None:
        self.agents: Dict[str, AgentSpec] = {agent.name: agent for agent in agents}
        self.reviewer_name = reviewer_name
        self.ambiguity_threshold = ambiguity_threshold
        self._validate()

    def _validate(self) -> None:
        if not self.agents:
            raise ArchitectureError("At least one agent is required.")
        if self.reviewer_name not in self.agents:
            raise ArchitectureError("A reviewer agent is required.")
        for agent in self.agents.values():
            if not agent.name.strip():
                raise ArchitectureError("Agent name cannot be empty.")
            if not agent.role.strip():
                raise ArchitectureError(f"Agent {agent.name} must have a role.")
            if agent.name != self.reviewer_name and not agent.keywords:
                raise ArchitectureError(f"Agent {agent.name} must define routing keywords.")

    def route(self, task: Task) -> RoutingDecision:
        scores: List[Tuple[str, int]] = [
            (agent.name, agent.matches(task.message))
            for agent in self.agents.values()
            if agent.name != self.reviewer_name
        ]
        scores.sort(key=lambda item: item[1], reverse=True)
        best_name, best_score = scores[0]

        if best_score == 0:
            return RoutingDecision(None, 0.0, "No specialist matched the request.", True)

        tied = [name for name, score in scores if score == best_score]
        total_matches = sum(score for _, score in scores)
        confidence = best_score / max(total_matches, 1)

        if len(tied) > 1 or confidence < self.ambiguity_threshold:
            return RoutingDecision(
                None,
                round(confidence, 2),
                f"Ambiguous routing between: {', '.join(tied)}.",
                True,
            )

        return RoutingDecision(best_name, round(confidence, 2), f"Best keyword match: {best_name}.", False)

    def run_specialist(self, agent_name: str, task: Task) -> AgentResult:
        if agent_name not in self.agents:
            raise ArchitectureError(f"Unknown agent: {agent_name}")
        agent = self.agents[agent_name]
        lower = task.message.lower()
        risk_level = "high" if any(word in lower for word in ("breach", "fraud", "legal")) else "low"
        requires_review = risk_level == "high"
        if requires_review:
            answer = f"{agent.role}: demande sensible détectée. Escalade recommandée pour le ticket {task.ticket_id}."
        else:
            answer = f"{agent.role}: réponse préparée pour le ticket {task.ticket_id}."
        return AgentResult(agent.name, answer, TaskStatus.COMPLETED, risk_level, requires_review)

    def review(self, result: AgentResult) -> AgentResult:
        if not result.answer.strip():
            return AgentResult("reviewer", "Réponse rejetée : contenu vide.", TaskStatus.REJECTED, "medium", True)
        suffix = " Revue humaine requise." if result.requires_human_review else " Réponse validée."
        return AgentResult(self.reviewer_name, result.answer + suffix, TaskStatus.COMPLETED, result.risk_level, result.requires_human_review)

    def run_manager_worker(self, task: Task) -> MultiAgentRun:
        trace: List[TraceEvent] = [TraceEvent(1, "manager", "receive_task", "ok", task.ticket_id)]
        routing = self.route(task)
        trace.append(TraceEvent(2, "router", "route", "clarification" if routing.requires_clarification else "ok", routing.reason))

        if routing.requires_clarification or routing.target_agent is None:
            final = "Pouvez-vous préciser votre demande afin de choisir le bon spécialiste ?"
            trace.append(TraceEvent(3, "manager", "ask_clarification", "needs_clarification", final))
            return MultiAgentRun(task, routing, None, False, final, trace)

        specialist_result = self.run_specialist(routing.target_agent, task)
        trace.append(TraceEvent(3, routing.target_agent, "solve", specialist_result.status.value, specialist_result.answer))
        reviewed = self.review(specialist_result)
        trace.append(TraceEvent(4, self.reviewer_name, "review", reviewed.status.value, reviewed.answer))
        trace.append(TraceEvent(5, "manager", "finalize", reviewed.status.value, reviewed.answer))
        return MultiAgentRun(task, routing, reviewed, True, reviewed.answer, trace)

    def run_handoff(self, task: Task) -> MultiAgentRun:
        trace: List[TraceEvent] = [TraceEvent(1, "triage", "receive_task", "ok", task.ticket_id)]
        routing = self.route(task)
        trace.append(TraceEvent(2, "triage", "handoff_decision", "clarification" if routing.requires_clarification else "ok", routing.reason))

        if routing.requires_clarification or routing.target_agent is None:
            final = "Le triage ne peut pas transférer sans précision supplémentaire."
            trace.append(TraceEvent(3, "triage", "ask_clarification", "needs_clarification", final))
            return MultiAgentRun(task, routing, None, False, final, trace)

        specialist_result = self.run_specialist(routing.target_agent, task)
        trace.append(TraceEvent(3, routing.target_agent, "take_control", specialist_result.status.value, specialist_result.answer))
        return MultiAgentRun(task, routing, specialist_result, False, specialist_result.answer, trace)

    def run_parallel_review(self, task: Task, selected_agents: Iterable[str]) -> List[AgentResult]:
        return [
            self.run_specialist(name, task)
            for name in selected_agents
            if name != self.reviewer_name
        ]


def build_default_architecture() -> MultiAgentArchitecture:
    agents = [
        AgentSpec("billing", "Billing Specialist", ("invoice", "billing", "payment", "subscription", "facture", "paiement"), ("get_invoice", "get_subscription")),
        AgentSpec("technical", "Technical Specialist", ("bug", "error", "crash", "latency", "technical", "erreur", "incident"), ("get_logs", "get_status_page")),
        AgentSpec("refund", "Refund Specialist", ("refund", "cancel", "money back", "remboursement", "annulation"), ("get_order", "get_refund_policy"), True),
        AgentSpec("product", "Product Specialist", ("feature", "roadmap", "improvement", "fonctionnalité", "produit"), ("get_roadmap",)),
        AgentSpec("reviewer", "Reviewer Agent", ()),
    ]
    return MultiAgentArchitecture(agents)


def demo() -> None:
    architecture = build_default_architecture()
    task = Task("T-1001", "I have a payment problem with my invoice.", "u-42")
    print(architecture.run_manager_worker(task).to_json())


if __name__ == "__main__":
    demo()
