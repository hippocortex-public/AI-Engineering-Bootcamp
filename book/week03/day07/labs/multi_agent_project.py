"""
Semaine 3 — Jour 7 — Projet multi-agent.

Lab autonome sans dépendance externe.

Objectif :
- simuler un projet multi-agent complet ;
- coordonner plusieurs rôles ;
- exposer des outils via une interface compatible MCP ;
- partager un état versionné ;
- construire un contexte filtré par agent ;
- produire une trace JSON et une revue finale.

Ce fichier est volontairement déterministe pour être testable.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, Iterable, List, Optional
import json
import re


VALID_STATUSES = {
    "completed",
    "needs_revision",
    "needs_clarification",
    "blocked_by_policy",
}

VISIBILITIES = {"private", "shared", "public"}


@dataclass(frozen=True)
class Task:
    """Unité de travail assignable à un agent."""

    title: str
    owner: str
    goal: str
    required_tools: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class Artifact:
    """Production intermédiaire ou finale d'un agent."""

    name: str
    kind: str
    content: Dict[str, Any]
    created_by: str


@dataclass(frozen=True)
class StateEntry:
    """Entrée d'état partagée et versionnée."""

    key: str
    value: Any
    owner: str
    visibility: str = "shared"
    version: int = 1
    readers: List[str] = field(default_factory=list)

    def is_visible_to(self, role: str) -> bool:
        if self.visibility == "public":
            return True
        if self.visibility == "private":
            return role == self.owner
        return role == self.owner or role in self.readers


@dataclass(frozen=True)
class Event:
    """Événement de trace."""

    step: int
    actor: str
    event: str
    detail: Dict[str, Any] = field(default_factory=dict)


class SharedStateStore:
    """Store d'état partagé avec visibilité et versionnement."""

    def __init__(self) -> None:
        self._entries: Dict[str, StateEntry] = {}
        self._events: List[Event] = []
        self._step = 0

    def put(
        self,
        key: str,
        value: Any,
        owner: str,
        visibility: str = "shared",
        readers: Optional[Iterable[str]] = None,
    ) -> StateEntry:
        if not key:
            raise ValueError("state key must not be empty")
        if visibility not in VISIBILITIES:
            raise ValueError(f"unsupported visibility: {visibility}")

        previous = self._entries.get(key)
        version = 1 if previous is None else previous.version + 1
        entry = StateEntry(
            key=key,
            value=value,
            owner=owner,
            visibility=visibility,
            version=version,
            readers=sorted(set(readers or [])),
        )
        self._entries[key] = entry
        self.record(owner, "state_written", {"key": key, "version": version, "visibility": visibility})
        return entry

    def get(self, key: str, role: str) -> Any:
        entry = self._entries[key]
        if not entry.is_visible_to(role):
            raise PermissionError(f"{role} cannot read {key}")
        return entry.value

    def snapshot_for(self, role: str) -> Dict[str, Any]:
        return {
            key: entry.value
            for key, entry in sorted(self._entries.items())
            if entry.is_visible_to(role)
        }

    def entries_for(self, role: str) -> List[StateEntry]:
        return [
            entry
            for _, entry in sorted(self._entries.items())
            if entry.is_visible_to(role)
        ]

    def record(self, actor: str, event: str, detail: Optional[Dict[str, Any]] = None) -> Event:
        self._step += 1
        item = Event(step=self._step, actor=actor, event=event, detail=detail or {})
        self._events.append(item)
        return item

    def trace(self) -> List[Dict[str, Any]]:
        return [asdict(event) for event in self._events]


@dataclass(frozen=True)
class ToolSpec:
    """Description d'un outil exposé via l'adaptateur MCP pédagogique."""

    name: str
    description: str
    required: List[str]
    handler: Callable[[Dict[str, Any]], Dict[str, Any]]
    sensitive: bool = False


class MCPToolAdapter:
    """Client MCP pédagogique.

    Il ne parle pas à un serveur réel. Il simule les opérations essentielles :
    découverte d'outils, validation d'arguments, blocage des actions sensibles
    et appel déterministe de handler.
    """

    def __init__(self, tools: Iterable[ToolSpec], state: SharedStateStore):
        self._tools = {tool.name: tool for tool in tools}
        self._state = state

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "required": list(tool.required),
                "sensitive": tool.sensitive,
            }
            for name, tool in sorted(self._tools.items())
        ]

    def call(
        self,
        name: str,
        arguments: Dict[str, Any],
        actor: str,
        approved: bool = False,
    ) -> Dict[str, Any]:
        if name not in self._tools:
            raise KeyError(f"unknown tool: {name}")
        tool = self._tools[name]

        missing = [field_name for field_name in tool.required if field_name not in arguments]
        if missing:
            raise ValueError(f"missing required arguments for {name}: {', '.join(missing)}")

        if tool.sensitive and not approved:
            self._state.record(actor, "tool_blocked", {"tool": name, "reason": "approval_required"})
            return {
                "status": "blocked_by_policy",
                "tool": name,
                "reason": "human approval required",
            }

        self._state.record(actor, "tool_called", {"tool": name, "arguments": sorted(arguments)})
        result = tool.handler(arguments)
        self._state.record(actor, "tool_completed", {"tool": name})
        return result


class ContextBuilder:
    """Construit un context pack filtré par rôle et budget."""

    def __init__(self, state: SharedStateStore, max_chars: int = 1200):
        if max_chars < 200:
            raise ValueError("max_chars must be at least 200 for this lab")
        self.state = state
        self.max_chars = max_chars

    def build(self, role: str, task: Task, available_tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        entries = self.state.entries_for(role)
        context_items = []
        used = 0

        # Les entrées publiques et partagées à forte priorité apparaissent d'abord.
        for entry in entries:
            serialized = json.dumps(entry.value, ensure_ascii=False, sort_keys=True)
            cost = len(entry.key) + len(serialized)
            if used + cost > self.max_chars:
                continue
            context_items.append(
                {
                    "key": entry.key,
                    "value": entry.value,
                    "owner": entry.owner,
                    "visibility": entry.visibility,
                    "version": entry.version,
                }
            )
            used += cost

        tools_for_task = [
            tool
            for tool in available_tools
            if tool["name"] in task.required_tools
        ]

        return {
            "role": role,
            "task": asdict(task),
            "state": context_items,
            "tools": tools_for_task,
            "budget": {"max_chars": self.max_chars, "used_chars": used},
        }


class PlannerAgent:
    role = "planner"

    def run(self, objective: str) -> List[Task]:
        normalized = objective.lower()
        tasks = [
            Task(
                title="delivery_plan",
                owner="planner",
                goal="Découper la demande en livrables contrôlés.",
            ),
            Task(
                title="research_notes",
                owner="researcher",
                goal="Extraire les contraintes et ressources utiles.",
                required_tools=["search_knowledge_base"],
                depends_on=["delivery_plan"],
            ),
            Task(
                title="architecture_proposal",
                owner="engineer",
                goal="Proposer une architecture multi-agent exploitable.",
                required_tools=["generate_architecture"],
                depends_on=["research_notes"],
            ),
            Task(
                title="test_plan",
                owner="engineer",
                goal="Définir une stratégie de validation.",
                required_tools=["create_test_plan"],
                depends_on=["architecture_proposal"],
            ),
            Task(
                title="security_review",
                owner="security",
                goal="Identifier les risques et actions sensibles.",
                depends_on=["architecture_proposal"],
            ),
            Task(
                title="final_review",
                owner="reviewer",
                goal="Évaluer la complétude et la cohérence du résultat.",
                depends_on=["architecture_proposal", "security_review", "test_plan"],
            ),
        ]

        if "deploy" in normalized or "déploi" in normalized:
            tasks.insert(
                -1,
                Task(
                    title="deployment_approval",
                    owner="security",
                    goal="Demander une validation humaine avant action sensible.",
                    required_tools=["request_human_approval"],
                    depends_on=["security_review"],
                ),
            )

        return tasks


class ResearcherAgent:
    role = "researcher"

    def run(self, task: Task, context: Dict[str, Any], tools: MCPToolAdapter) -> Artifact:
        objective = _objective_from_context(context)
        result = tools.call(
            "search_knowledge_base",
            {"query": objective},
            actor=self.role,
        )
        return Artifact(
            name=task.title,
            kind="research",
            created_by=self.role,
            content={
                "summary": result["summary"],
                "constraints": result["constraints"],
                "sources": result["sources"],
            },
        )


class EngineerAgent:
    role = "engineer"

    def run(self, task: Task, context: Dict[str, Any], tools: MCPToolAdapter) -> Artifact:
        objective = _objective_from_context(context)

        if task.title == "test_plan":
            result = tools.call(
                "create_test_plan",
                {"artifact_name": "architecture_proposal"},
                actor=self.role,
            )
            return Artifact(
                name=task.title,
                kind="testing",
                created_by=self.role,
                content=result,
            )

        constraints = []
        for item in context["state"]:
            if item["key"] == "research_notes":
                constraints.extend(item["value"].get("constraints", []))

        result = tools.call(
            "generate_architecture",
            {"objective": objective, "constraints": constraints},
            actor=self.role,
        )
        return Artifact(
            name=task.title,
            kind="architecture",
            created_by=self.role,
            content=result,
        )


class SecurityAgent:
    role = "security"

    def run(
        self,
        task: Task,
        context: Dict[str, Any],
        tools: MCPToolAdapter,
        approved: bool = False,
    ) -> Artifact:
        objective = _objective_from_context(context).lower()

        if task.title == "deployment_approval":
            result = tools.call(
                "request_human_approval",
                {"action": "deployment", "reason": "action sensible détectée dans l'objectif"},
                actor=self.role,
                approved=approved,
            )
            return Artifact(
                name=task.title,
                kind="approval",
                created_by=self.role,
                content=result,
            )

        risks = ["tool misuse", "context leakage", "unbounded autonomy"]
        if "customer" in objective or "client" in objective:
            risks.append("personal data exposure")
        if "deploy" in objective or "déploi" in objective:
            risks.append("deployment requires human approval")

        return Artifact(
            name=task.title,
            kind="security",
            created_by=self.role,
            content={
                "risks": risks,
                "blocked": False,
                "recommendations": [
                    "limit context by role",
                    "require approval for sensitive tools",
                    "export execution trace",
                ],
            },
        )


class ReviewerAgent:
    role = "reviewer"

    def run(self, task: Task, context: Dict[str, Any]) -> Artifact:
        visible_names = {
            item["key"]
            for item in context["state"]
        }
        required = {
            "delivery_plan",
            "research_notes",
            "architecture_proposal",
            "test_plan",
            "security_review",
        }
        missing = sorted(required - visible_names)
        score = 1.0 - (0.15 * len(missing))

        if "blocked_policy" in visible_names or "deployment_approval" in visible_names:
            approval_entries = [
                item for item in context["state"] if item["key"] == "deployment_approval"
            ]
            if approval_entries and approval_entries[0]["value"].get("status") == "blocked_by_policy":
                score -= 0.4
                missing.append("human approval")

        verdict = "approved" if score >= 0.8 and not missing else "needs_revision"
        comments = ["Architecture multi-agent traçable et testable."]
        if missing:
            comments.append(f"Éléments à compléter: {', '.join(missing)}")

        return Artifact(
            name=task.title,
            kind="review",
            created_by=self.role,
            content={
                "score": round(max(score, 0.0), 2),
                "verdict": verdict,
                "comments": comments,
            },
        )


class DeliveryCoordinator:
    """Orchestrateur principal du projet multi-agent."""

    def __init__(self, max_context_chars: int = 10000):
        self.state = SharedStateStore()
        self.tools = MCPToolAdapter(default_tools(), self.state)
        self.context_builder = ContextBuilder(self.state, max_chars=max_context_chars)
        self.planner = PlannerAgent()
        self.agents = {
            "researcher": ResearcherAgent(),
            "engineer": EngineerAgent(),
            "security": SecurityAgent(),
            "reviewer": ReviewerAgent(),
        }

    def run(self, objective: str, approved_actions: bool = False) -> Dict[str, Any]:
        objective = objective.strip()
        if not objective:
            raise ValueError("objective must not be empty")

        if len(objective) < 20:
            self.state.record("coordinator", "needs_clarification", {"reason": "objective too short"})
            return {
                "status": "needs_clarification",
                "objective": objective,
                "artifacts": [],
                "review": {
                    "score": 0.0,
                    "verdict": "needs_clarification",
                    "comments": ["Objectif trop court pour lancer un projet multi-agent."],
                },
                "trace": self.state.trace(),
            }

        self.state.record("coordinator", "run_started", {"objective_hash": stable_hash(objective)})
        self.state.put("objective", objective, owner="coordinator", visibility="public")

        tasks = self.planner.run(objective)
        plan_payload = [asdict(task) for task in tasks]
        self.state.put("delivery_plan", {"tasks": plan_payload}, owner="planner", visibility="public")
        self.state.record("planner", "plan_created", {"task_count": len(tasks)})

        artifacts: List[Artifact] = [
            Artifact(
                name="delivery_plan",
                kind="plan",
                created_by="planner",
                content={"tasks": plan_payload},
            )
        ]

        for task in tasks:
            if task.owner == "planner":
                continue

            available_tools = self.tools.list_tools()
            context = self.context_builder.build(task.owner, task, available_tools)
            self.state.record(
                "coordinator",
                "context_built",
                {
                    "for": task.owner,
                    "task": task.title,
                    "used_chars": context["budget"]["used_chars"],
                    "tool_count": len(context["tools"]),
                },
            )

            agent = self.agents[task.owner]
            if isinstance(agent, SecurityAgent):
                artifact = agent.run(task, context, self.tools, approved=approved_actions)
            elif isinstance(agent, ReviewerAgent):
                artifact = agent.run(task, context)
            else:
                artifact = agent.run(task, context, self.tools)

            artifacts.append(artifact)

            visibility = "public" if artifact.kind in {"plan", "review"} else "shared"
            readers = ["reviewer", "security", "engineer", "researcher"]
            self.state.put(
                artifact.name,
                artifact.content,
                owner=artifact.created_by,
                visibility=visibility,
                readers=readers,
            )
            self.state.record(
                artifact.created_by,
                "artifact_created",
                {"artifact": artifact.name, "kind": artifact.kind},
            )

            if artifact.content.get("status") == "blocked_by_policy":
                review = {
                    "score": 0.0,
                    "verdict": "blocked_by_policy",
                    "comments": ["Action sensible bloquée faute d'approbation humaine."],
                }
                return self._finalize(
                    status="blocked_by_policy",
                    objective=objective,
                    artifacts=artifacts,
                    review=review,
                )

        final_review = next((a for a in artifacts if a.name == "final_review"), None)
        if final_review is None:
            status = "needs_revision"
            review = {
                "score": 0.0,
                "verdict": "needs_revision",
                "comments": ["Revue finale absente."],
            }
        else:
            review = final_review.content
            status = "completed" if review["verdict"] == "approved" else "needs_revision"

        return self._finalize(status=status, objective=objective, artifacts=artifacts, review=review)

    def _finalize(
        self,
        status: str,
        objective: str,
        artifacts: List[Artifact],
        review: Dict[str, Any],
    ) -> Dict[str, Any]:
        if status not in VALID_STATUSES:
            raise ValueError(f"invalid status: {status}")

        self.state.record("coordinator", "run_finished", {"status": status})
        return {
            "status": status,
            "objective": objective,
            "artifacts": [asdict(artifact) for artifact in artifacts],
            "review": review,
            "trace": self.state.trace(),
        }


def _objective_from_context(context: Dict[str, Any]) -> str:
    for item in context["state"]:
        if item["key"] == "objective":
            return str(item["value"])
    return context["task"]["goal"]


def stable_hash(text: str) -> str:
    """Hash court et déterministe pour tracer un objectif sans le recopier partout."""

    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def default_tools() -> List[ToolSpec]:
    return [
        ToolSpec(
            name="create_test_plan",
            description="Crée un plan de test pour un artefact technique.",
            required=["artifact_name"],
            handler=create_test_plan,
            sensitive=False,
        ),
        ToolSpec(
            name="generate_architecture",
            description="Génère une architecture multi-agent pédagogique.",
            required=["objective", "constraints"],
            handler=generate_architecture,
            sensitive=False,
        ),
        ToolSpec(
            name="request_human_approval",
            description="Demande une validation humaine pour une action sensible.",
            required=["action", "reason"],
            handler=request_human_approval,
            sensitive=True,
        ),
        ToolSpec(
            name="search_knowledge_base",
            description="Recherche des contraintes de conception dans une base documentaire simulée.",
            required=["query"],
            handler=search_knowledge_base,
            sensitive=False,
        ),
    ]


def search_knowledge_base(arguments: Dict[str, Any]) -> Dict[str, Any]:
    query = arguments["query"].lower()
    constraints = [
        "séparer agents et outils",
        "limiter le contexte par rôle",
        "tracer les décisions",
    ]

    if "mcp" in query:
        constraints.append("exposer les capacités via tools standardisés")
    if "state" in query or "état" in query:
        constraints.append("versionner l'état partagé")
    if "security" in query or "sécurité" in query:
        constraints.append("bloquer les actions sensibles sans approbation")

    return {
        "summary": "Contraintes d'architecture multi-agent extraites de la base simulée.",
        "constraints": constraints,
        "sources": ["roadmap_week03", "mcp_design_notes", "context_engineering_notes"],
    }


def generate_architecture(arguments: Dict[str, Any]) -> Dict[str, Any]:
    constraints = arguments["constraints"]
    components = [
        "DeliveryCoordinator",
        "PlannerAgent",
        "ResearcherAgent",
        "EngineerAgent",
        "SecurityAgent",
        "ReviewerAgent",
        "SharedStateStore",
        "ContextBuilder",
        "MCPToolAdapter",
    ]

    return {
        "style": "coordinator-led multi-agent architecture",
        "components": components,
        "constraints_applied": constraints,
        "handoff_policy": "centralized via coordinator",
        "state_policy": "public/shared/private entries with versions",
    }


def create_test_plan(arguments: Dict[str, Any]) -> Dict[str, Any]:
    artifact = arguments["artifact_name"]
    return {
        "artifact_name": artifact,
        "tests": [
            "valid objective produces completed status",
            "short objective asks for clarification",
            "sensitive tool is blocked without approval",
            "context excludes private state from other roles",
            "trace is JSON serializable",
        ],
    }


def request_human_approval(arguments: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "approved",
        "action": arguments["action"],
        "reason": arguments["reason"],
        "approved_by": "human_reviewer",
    }


def summarize_result(result: Dict[str, Any]) -> str:
    """Résumé lisible d'un résultat de projet."""

    artifact_names = [artifact["name"] for artifact in result["artifacts"]]
    return (
        f"Statut: {result['status']}\n"
        f"Artefacts: {', '.join(artifact_names)}\n"
        f"Score review: {result['review']['score']}"
    )


def main() -> None:
    coordinator = DeliveryCoordinator()
    result = coordinator.run(
        "Concevoir un assistant multi-agent avec MCP, état partagé, contexte contrôlé, sécurité et revue finale."
    )
    print(summarize_result(result))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
