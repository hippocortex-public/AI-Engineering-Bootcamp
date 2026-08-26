"""
Semaine 3 — Jour 2 — Coordination multi-agents.

Ce module illustre une coordination multi-agent déterministe.
Il n'appelle aucun LLM et ne dépend d'aucune bibliothèque externe.

Objectif pédagogique :
- séparer agents, registre, politique et coordinateur ;
- produire un plan de coordination explicite ;
- détecter les conflits ;
- déclencher une revue ;
- générer une trace JSON exploitable.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, Iterable, List, Optional, Sequence
import json


VALID_RISK_LEVELS = {"low", "medium", "high"}
CONFLICTING_STATUS_PAIRS = {
    frozenset(("resolved", "unresolved")),
    frozenset(("approved", "blocked")),
    frozenset(("safe", "unsafe")),
    frozenset(("ready", "missing_information")),
}


@dataclass(frozen=True)
class CoordinationTask:
    """Tâche structurée reçue par le coordinateur."""

    task_id: str
    objective: str
    domains: List[str]
    risk_level: str = "low"
    constraints: List[str] = field(default_factory=list)
    sensitive_action: bool = False

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ValueError("task_id must not be empty")
        if not self.objective.strip():
            raise ValueError("objective must not be empty")
        if self.risk_level not in VALID_RISK_LEVELS:
            raise ValueError(f"risk_level must be one of {sorted(VALID_RISK_LEVELS)}")


@dataclass(frozen=True)
class AgentContext:
    """Vue filtrée transmise à un agent."""

    task_id: str
    objective: str
    domains: List[str]
    risk_level: str
    constraints: List[str]


@dataclass(frozen=True)
class AgentObservation:
    """Observation produite par un agent spécialiste."""

    agent: str
    status: str
    finding: str
    confidence: float
    domains: List[str]

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class CoordinationPlan:
    """Plan d'exécution construit par le coordinateur."""

    task_id: str
    objective: str
    selected_agents: List[str]
    execution_mode: str
    requires_review: bool
    max_rounds: int
    review_reasons: List[str]

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class CoordinationResult:
    """Résultat final de coordination."""

    task_id: str
    status: str
    selected_agents: List[str]
    review_performed: bool
    conflicts: List[str]
    final_answer: str
    observations: List[AgentObservation]
    trace: List[Dict[str, object]]

    def to_dict(self) -> Dict[str, object]:
        return {
            "task_id": self.task_id,
            "status": self.status,
            "selected_agents": list(self.selected_agents),
            "review_performed": self.review_performed,
            "conflicts": list(self.conflicts),
            "final_answer": self.final_answer,
            "observations": [observation.to_dict() for observation in self.observations],
            "trace": list(self.trace),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class SpecialistAgent:
    """Agent spécialiste déterministe.

    Dans un système réel, cette classe pourrait appeler un LLM ou un outil MCP.
    Ici, elle retourne une observation stable pour tester la coordination.
    """

    def __init__(
        self,
        name: str,
        domains: Sequence[str],
        default_status: str,
        summary_template: str,
        confidence: float = 0.8,
    ) -> None:
        self.name = name
        self.domains = list(domains)
        self.default_status = default_status
        self.summary_template = summary_template
        self.confidence = confidence

    def supports_any(self, domains: Iterable[str]) -> bool:
        requested = set(domains)
        return any(domain in requested for domain in self.domains)

    def build_context(self, task: CoordinationTask) -> AgentContext:
        matching_domains = [domain for domain in task.domains if domain in self.domains]
        return AgentContext(
            task_id=task.task_id,
            objective=task.objective,
            domains=matching_domains,
            risk_level=task.risk_level,
            constraints=list(task.constraints),
        )

    def run(self, context: AgentContext) -> AgentObservation:
        finding = self.summary_template.format(
            task_id=context.task_id,
            objective=context.objective,
            domains=", ".join(context.domains) or "general",
            risk_level=context.risk_level,
        )
        return AgentObservation(
            agent=self.name,
            status=self.default_status,
            finding=finding,
            confidence=self.confidence,
            domains=list(context.domains),
        )


class ReviewerAgent(SpecialistAgent):
    """Agent de revue déterministe."""

    def __init__(self) -> None:
        super().__init__(
            name="reviewer_agent",
            domains=["review"],
            default_status="reviewed",
            summary_template="Review completed for task {task_id}.",
            confidence=0.9,
        )

    def review(
        self,
        task: CoordinationTask,
        observations: Sequence[AgentObservation],
        conflicts: Sequence[str],
        reasons: Sequence[str],
    ) -> AgentObservation:
        if conflicts:
            status = "needs_clarification"
            finding = (
                f"Review found unresolved coordination conflicts for {task.task_id}: "
                + "; ".join(conflicts)
            )
        elif task.risk_level == "high" or task.sensitive_action:
            status = "caution"
            finding = (
                f"Review completed for high-risk task {task.task_id}. "
                f"Reasons: {', '.join(reasons) or 'risk policy'}."
            )
        elif not observations:
            status = "missing_information"
            finding = f"Review could not validate {task.task_id} because no specialist was selected."
        else:
            status = "reviewed"
            finding = f"Review completed for task {task.task_id}; no blocking issue detected."

        return AgentObservation(
            agent=self.name,
            status=status,
            finding=finding,
            confidence=0.9,
            domains=["review"],
        )


class AgentRegistry:
    """Registre des agents disponibles."""

    def __init__(self) -> None:
        self._agents: Dict[str, SpecialistAgent] = {}

    def register(self, agent: SpecialistAgent) -> None:
        if agent.name in self._agents:
            raise ValueError(f"Agent already registered: {agent.name}")
        self._agents[agent.name] = agent

    def get(self, name: str) -> SpecialistAgent:
        return self._agents[name]

    def select_by_domains(self, domains: Sequence[str]) -> List[SpecialistAgent]:
        selected = [
            agent
            for agent in self._agents.values()
            if agent.name != "reviewer_agent" and agent.supports_any(domains)
        ]
        return sorted(selected, key=lambda agent: agent.name)

    @property
    def names(self) -> List[str]:
        return sorted(self._agents)


class CoordinationPolicy:
    """Politique de coordination.

    Elle décide :
    - du mode d'exécution ;
    - des raisons de revue ;
    - du statut final.
    """

    def __init__(self, max_rounds: int = 2) -> None:
        if max_rounds < 1:
            raise ValueError("max_rounds must be >= 1")
        self.max_rounds = max_rounds

    def execution_mode_for(self, selected_agents: Sequence[SpecialistAgent]) -> str:
        if len(selected_agents) <= 1:
            return "sequential"
        return "parallel"

    def review_reasons(
        self,
        task: CoordinationTask,
        selected_agent_names: Sequence[str],
        conflicts: Sequence[str],
    ) -> List[str]:
        reasons: List[str] = []

        if task.risk_level == "high":
            reasons.append("high_risk")

        if conflicts:
            reasons.append("conflict_detected")

        if task.sensitive_action:
            reasons.append("sensitive_action")

        if "security_agent" in selected_agent_names:
            reasons.append("security_domain")

        if not selected_agent_names:
            reasons.append("no_specialist_selected")

        if any("enterprise" in constraint.lower() for constraint in task.constraints):
            reasons.append("enterprise_external_response")

        return reasons

    def status_for(
        self,
        review_performed: bool,
        conflicts: Sequence[str],
        observations: Sequence[AgentObservation],
    ) -> str:
        if conflicts:
            return "needs_clarification"

        if not observations:
            return "needs_clarification"

        specialist_observations = [
            observation for observation in observations if observation.agent != "reviewer_agent"
        ]
        if not specialist_observations:
            return "needs_clarification"

        statuses = {observation.status for observation in observations}

        if "needs_clarification" in statuses or "missing_information" in statuses:
            return "needs_clarification"

        if "blocked" in statuses or "unsafe" in statuses:
            return "needs_review"

        if review_performed:
            return "needs_review"

        return "completed"


class MultiAgentCoordinator:
    """Coordinateur multi-agent minimal."""

    def __init__(self, registry: AgentRegistry, policy: Optional[CoordinationPolicy] = None) -> None:
        self.registry = registry
        self.policy = policy or CoordinationPolicy()

    def build_plan(self, task: CoordinationTask) -> CoordinationPlan:
        selected_agents = self.registry.select_by_domains(task.domains)
        selected_names = [agent.name for agent in selected_agents]
        preliminary_reasons = self.policy.review_reasons(task, selected_names, conflicts=[])

        return CoordinationPlan(
            task_id=task.task_id,
            objective=task.objective,
            selected_agents=selected_names,
            execution_mode=self.policy.execution_mode_for(selected_agents),
            requires_review=bool(preliminary_reasons),
            max_rounds=self.policy.max_rounds,
            review_reasons=preliminary_reasons,
        )

    def run(self, task: CoordinationTask) -> CoordinationResult:
        trace: List[Dict[str, object]] = [
            {"type": "task_received", "task_id": task.task_id, "domains": list(task.domains)}
        ]

        plan = self.build_plan(task)
        trace.append({"type": "plan_created", "plan": plan.to_dict()})

        observations: List[AgentObservation] = []
        for agent_name in plan.selected_agents:
            agent = self.registry.get(agent_name)
            context = agent.build_context(task)
            trace.append(
                {
                    "type": "agent_context_built",
                    "agent": agent.name,
                    "context": asdict(context),
                }
            )
            observation = agent.run(context)
            observations.append(observation)
            trace.append(
                {
                    "type": "agent_completed",
                    "agent": agent.name,
                    "status": observation.status,
                    "confidence": observation.confidence,
                }
            )

        conflicts = detect_conflicts(observations)
        trace.append({"type": "conflict_check", "conflicts": list(conflicts)})

        selected_names = [observation.agent for observation in observations]
        review_reasons = self.policy.review_reasons(task, selected_names, conflicts)
        review_performed = bool(review_reasons)

        if review_performed:
            reviewer = self.registry.get("reviewer_agent")
            if not isinstance(reviewer, ReviewerAgent):
                raise TypeError("reviewer_agent must be a ReviewerAgent")
            review_observation = reviewer.review(task, observations, conflicts, review_reasons)
            observations.append(review_observation)
            trace.append(
                {
                    "type": "review_performed",
                    "agent": reviewer.name,
                    "reasons": review_reasons,
                    "status": review_observation.status,
                }
            )
        else:
            trace.append({"type": "review_skipped", "reason": "policy_not_triggered"})

        status = self.policy.status_for(review_performed, conflicts, observations)
        final_answer = synthesize_final_answer(
            task=task,
            observations=observations,
            conflicts=conflicts,
            review_performed=review_performed,
        )

        trace.append({"type": "final_answer_created", "status": status})

        return CoordinationResult(
            task_id=task.task_id,
            status=status,
            selected_agents=selected_names,
            review_performed=review_performed,
            conflicts=list(conflicts),
            final_answer=final_answer,
            observations=observations,
            trace=trace,
        )


def detect_conflicts(observations: Sequence[AgentObservation]) -> List[str]:
    """Détecte des conflits simples à partir des statuts."""

    conflicts: List[str] = []
    statuses_by_agent = {observation.agent: observation.status for observation in observations}

    for left_agent, left_status in statuses_by_agent.items():
        for right_agent, right_status in statuses_by_agent.items():
            if left_agent >= right_agent:
                continue
            pair = frozenset((left_status, right_status))
            if pair in CONFLICTING_STATUS_PAIRS:
                conflicts.append(
                    f"{left_agent}:{left_status} conflicts with {right_agent}:{right_status}"
                )

    return conflicts


def synthesize_final_answer(
    task: CoordinationTask,
    observations: Sequence[AgentObservation],
    conflicts: Sequence[str],
    review_performed: bool,
) -> str:
    """Produit une réponse finale lisible et déterministe."""

    if not observations:
        return (
            f"Task {task.task_id} needs clarification because no specialist could be selected."
        )

    if conflicts:
        return (
            f"Task {task.task_id} needs clarification before a final decision. "
            f"Detected conflicts: {'; '.join(conflicts)}."
        )

    specialist_findings = [
        observation.finding
        for observation in observations
        if observation.agent != "reviewer_agent"
    ]

    review_note = ""
    if review_performed:
        review_observations = [
            observation.finding
            for observation in observations
            if observation.agent == "reviewer_agent"
        ]
        if review_observations:
            review_note = " Review note: " + review_observations[-1]

    joined_findings = " ".join(specialist_findings)
    return f"Task {task.task_id} coordinated successfully. {joined_findings}{review_note}".strip()


def build_default_registry() -> AgentRegistry:
    """Construit le registre utilisé dans les exercices et les tests."""

    registry = AgentRegistry()

    registry.register(
        SpecialistAgent(
            name="billing_agent",
            domains=["billing", "payment", "invoice"],
            default_status="ready",
            summary_template="Billing analysis for {task_id}: invoice/payment facts checked.",
            confidence=0.82,
        )
    )
    registry.register(
        SpecialistAgent(
            name="engineering_agent",
            domains=["engineering", "bug", "api", "incident"],
            default_status="resolved",
            summary_template="Engineering analysis for {task_id}: technical investigation completed.",
            confidence=0.78,
        )
    )
    registry.register(
        SpecialistAgent(
            name="product_agent",
            domains=["product", "roadmap", "feedback"],
            default_status="ready",
            summary_template="Product analysis for {task_id}: product implications summarized.",
            confidence=0.75,
        )
    )
    registry.register(
        SpecialistAgent(
            name="security_agent",
            domains=["security", "access", "permission", "data"],
            default_status="caution",
            summary_template="Security analysis for {task_id}: sensitive constraints identified.",
            confidence=0.86,
        )
    )
    registry.register(
        SpecialistAgent(
            name="support_agent",
            domains=["support", "customer", "response"],
            default_status="ready",
            summary_template="Support analysis for {task_id}: customer response prepared.",
            confidence=0.8,
        )
    )
    registry.register(ReviewerAgent())

    return registry


def demo() -> None:
    """Démonstration locale."""

    registry = build_default_registry()
    coordinator = MultiAgentCoordinator(registry)

    task = CoordinationTask(
        task_id="demo-001",
        objective="Prepare a customer response about a duplicated payment and possible API incident.",
        domains=["support", "billing", "engineering"],
        risk_level="medium",
        constraints=["External enterprise response", "Do not promise refund automatically."],
    )

    result = coordinator.run(task)
    print(result.to_json())


if __name__ == "__main__":
    demo()
