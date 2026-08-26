"""
Semaine 4 — Jour 1 — Architecture d'un mini-framework d'agents.

Ce module ne construit pas encore un runner complet.
Il formalise l'architecture cible du framework et vérifie ses invariants.

Exécution :

    python mini_framework_architecture.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import json


REQUIRED_COMPONENTS = {
    "agent_definition",
    "runner",
    "model_client",
    "tool_registry",
    "memory_store",
    "workflow_engine",
    "observability",
}


@dataclass(frozen=True)
class ComponentSpec:
    """Description stable d'un composant du framework."""

    name: str
    responsibility: str
    interfaces: tuple[str, ...] = field(default_factory=tuple)
    depends_on: tuple[str, ...] = field(default_factory=tuple)
    risks: tuple[str, ...] = field(default_factory=tuple)

    def validate(self) -> list[str]:
        """Valide le composant indépendamment du graphe global."""
        errors: list[str] = []
        if not self.name.strip():
            errors.append("component.name is required")
        if not self.responsibility.strip():
            errors.append(f"{self.name}: responsibility is required")
        if not self.interfaces:
            errors.append(f"{self.name}: at least one interface is required")
        if self.name in self.depends_on:
            errors.append(f"{self.name}: component cannot depend on itself")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "responsibility": self.responsibility,
            "interfaces": list(self.interfaces),
            "depends_on": list(self.depends_on),
            "risks": list(self.risks),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ComponentSpec":
        return cls(
            name=str(payload["name"]),
            responsibility=str(payload["responsibility"]),
            interfaces=tuple(payload.get("interfaces", ())),
            depends_on=tuple(payload.get("depends_on", ())),
            risks=tuple(payload.get("risks", ())),
        )


@dataclass(frozen=True)
class DecisionRecord:
    """Architecture Decision Record simplifié."""

    identifier: str
    decision: str
    reason: str
    tradeoff: str

    def validate(self) -> list[str]:
        errors: list[str] = []
        for field_name in ("identifier", "decision", "reason", "tradeoff"):
            if not getattr(self, field_name).strip():
                errors.append(f"decision.{field_name} is required")
        return errors

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.identifier,
            "decision": self.decision,
            "reason": self.reason,
            "tradeoff": self.tradeoff,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, str]) -> "DecisionRecord":
        return cls(
            identifier=payload["id"],
            decision=payload["decision"],
            reason=payload["reason"],
            tradeoff=payload["tradeoff"],
        )


@dataclass
class ArchitectureBlueprint:
    """Blueprint d'architecture pour le mini-framework."""

    title: str
    objective: str
    components: list[ComponentSpec]
    decisions: list[DecisionRecord]
    invariants: list[str]

    def component_names(self) -> set[str]:
        return {component.name for component in self.components}

    def dependency_graph(self) -> dict[str, list[str]]:
        return {
            component.name: list(component.depends_on)
            for component in self.components
        }

    def validate(self) -> list[str]:
        """Valide les invariants d'architecture vérifiables."""
        errors: list[str] = []

        if not self.title.strip():
            errors.append("architecture.title is required")
        if not self.objective.strip():
            errors.append("architecture.objective is required")

        names = [component.name for component in self.components]
        duplicates = sorted({name for name in names if names.count(name) > 1})
        for duplicate in duplicates:
            errors.append(f"duplicate component: {duplicate}")

        for component in self.components:
            errors.extend(component.validate())

        available = set(names)
        missing_required = sorted(REQUIRED_COMPONENTS - available)
        for missing in missing_required:
            errors.append(f"missing required component: {missing}")

        for component in self.components:
            for dependency in component.depends_on:
                if dependency not in available:
                    errors.append(
                        f"{component.name}: unknown dependency '{dependency}'"
                    )

        errors.extend(self._detect_cycles())

        for decision in self.decisions:
            errors.extend(decision.validate())

        if len(self.invariants) < 3:
            errors.append("at least three architecture invariants are required")

        return errors

    def _detect_cycles(self) -> list[str]:
        graph = self.dependency_graph()
        visiting: set[str] = set()
        visited: set[str] = set()
        errors: list[str] = []

        def visit(node: str, path: list[str]) -> None:
            if node in visiting:
                cycle = path[path.index(node):] + [node]
                errors.append("cyclic dependency: " + " -> ".join(cycle))
                return
            if node in visited:
                return

            visiting.add(node)
            for dependency in graph.get(node, []):
                if dependency in graph:
                    visit(dependency, path + [dependency])
            visiting.remove(node)
            visited.add(node)

        for node in graph:
            visit(node, [node])
        return errors

    def topological_order(self) -> list[str]:
        """Retourne un ordre où les dépendances apparaissent avant leurs utilisateurs."""
        errors = self.validate()
        if errors:
            raise ValueError("invalid architecture: " + "; ".join(errors))

        graph = self.dependency_graph()
        permanent: set[str] = set()
        temporary: set[str] = set()
        ordered: list[str] = []

        def visit(node: str) -> None:
            if node in permanent:
                return
            if node in temporary:
                raise ValueError(f"cyclic dependency around {node}")
            temporary.add(node)
            for dependency in graph[node]:
                visit(dependency)
            temporary.remove(node)
            permanent.add(node)
            ordered.append(node)

        for name in graph:
            visit(name)

        return ordered

    def render_mermaid(self) -> str:
        """Produit un diagramme Mermaid simple de l'architecture."""
        lines = ["flowchart TD"]
        for component in sorted(self.components, key=lambda item: item.name):
            label = component.name.replace("_", " ").title()
            lines.append(f'    {component.name}["{label}"]')
        for component in sorted(self.components, key=lambda item: item.name):
            for dependency in component.depends_on:
                lines.append(f"    {component.name} --> {dependency}")
        return "\n".join(lines)

    def implementation_plan(self) -> list[str]:
        return [
            "Jour 2 — Implémenter AgentDefinition et les contrats d'agent.",
            "Jour 3 — Implémenter ToolRegistry, ToolSpec et validation d'arguments.",
            "Jour 4 — Ajouter MemoryStore et snapshots d'état.",
            "Jour 5 — Ajouter WorkflowEngine, transitions et limites d'exécution.",
            "Jour 6 — Ajouter Observability, traces et métriques.",
            "Jour 7 — Intégrer les composants dans un mini-framework cohérent.",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "objective": self.objective,
            "components": [component.to_dict() for component in self.components],
            "decisions": [decision.to_dict() for decision in self.decisions],
            "invariants": list(self.invariants),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ArchitectureBlueprint":
        return cls(
            title=str(payload["title"]),
            objective=str(payload["objective"]),
            components=[
                ComponentSpec.from_dict(item)
                for item in payload.get("components", [])
            ],
            decisions=[
                DecisionRecord.from_dict(item)
                for item in payload.get("decisions", [])
            ],
            invariants=list(payload.get("invariants", [])),
        )

    @classmethod
    def from_json(cls, payload: str) -> "ArchitectureBlueprint":
        return cls.from_dict(json.loads(payload))


class FrameworkArchitect:
    """Factory pédagogique pour produire l'architecture cible."""

    @staticmethod
    def default_blueprint() -> ArchitectureBlueprint:
        components = [
            ComponentSpec(
                name="application",
                responsibility="Expose les cas d'usage produit et appelle le framework.",
                interfaces=("run_use_case",),
                depends_on=("runner",),
                risks=("couplage métier-framework",),
            ),
            ComponentSpec(
                name="runner",
                responsibility="Orchestre l'exécution d'un agent sans logique métier spécifique.",
                interfaces=("run", "run_step"),
                depends_on=(
                    "agent_definition",
                    "model_client",
                    "tool_registry",
                    "memory_store",
                    "workflow_engine",
                    "observability",
                    "guardrails",
                ),
                risks=("classe trop grosse", "boucle infinie"),
            ),
            ComponentSpec(
                name="agent_definition",
                responsibility="Décrit un agent, ses instructions et ses capacités autorisées.",
                interfaces=("describe", "allowed_tools"),
                depends_on=(),
                risks=("prompt non versionné",),
            ),
            ComponentSpec(
                name="model_client",
                responsibility="Encapsule le fournisseur de modèle derrière une interface remplaçable.",
                interfaces=("generate",),
                depends_on=(),
                risks=("couplage fournisseur",),
            ),
            ComponentSpec(
                name="tool_registry",
                responsibility="Déclare les outils, schémas, permissions et fonctions exécutables.",
                interfaces=("register", "get", "call"),
                depends_on=(),
                risks=("outil sensible non protégé",),
            ),
            ComponentSpec(
                name="memory_store",
                responsibility="Isole l'état et la mémoire derrière un contrat explicite.",
                interfaces=("load", "save", "snapshot"),
                depends_on=(),
                risks=("fuite de données", "état global implicite"),
            ),
            ComponentSpec(
                name="workflow_engine",
                responsibility="Contrôle transitions, conditions d'arrêt et limites d'itérations.",
                interfaces=("next_step", "should_stop"),
                depends_on=(),
                risks=("boucle infinie", "condition d'arrêt floue"),
            ),
            ComponentSpec(
                name="observability",
                responsibility="Capture traces, erreurs et métriques sans modifier l'exécution.",
                interfaces=("record", "export"),
                depends_on=(),
                risks=("données sensibles dans les logs",),
            ),
            ComponentSpec(
                name="guardrails",
                responsibility="Contrôle entrées, sorties et appels sensibles.",
                interfaces=("check_input", "check_output", "check_tool_call"),
                depends_on=(),
                risks=("faux positifs", "faux négatifs"),
            ),
        ]

        decisions = [
            DecisionRecord(
                identifier="ADR-001",
                decision="Séparer AgentDefinition et Runner.",
                reason="Un agent doit rester déclaratif, testable et réutilisable.",
                tradeoff="Le contrat entre définition et exécution doit être explicite.",
            ),
            DecisionRecord(
                identifier="ADR-002",
                decision="Encapsuler le fournisseur modèle derrière ModelClient.",
                reason="Le framework doit être testable sans API externe et remplaçable.",
                tradeoff="Une couche d'adaptation supplémentaire doit être maintenue.",
            ),
            DecisionRecord(
                identifier="ADR-003",
                decision="Centraliser les outils dans ToolRegistry.",
                reason="Les schémas, permissions et métadonnées doivent être cohérents entre agents.",
                tradeoff="Le registre devient un composant critique à tester.",
            ),
        ]

        invariants = [
            "Les composants spécialisés ne dépendent pas du runner.",
            "Le runner orchestre sans logique métier spécifique.",
            "Le ModelClient est remplaçable.",
            "Les traces ne modifient jamais l'état métier.",
            "Les dépendances circulaires sont interdites.",
        ]

        return ArchitectureBlueprint(
            title="Architecture du mini-framework d'agents",
            objective=(
                "Définir un socle modulaire pour exécuter des agents avec modèle, "
                "outils, mémoire, workflow, garde-fous et observabilité."
            ),
            components=components,
            decisions=decisions,
            invariants=invariants,
        )


def build_default_architecture() -> ArchitectureBlueprint:
    return FrameworkArchitect.default_blueprint()


def main() -> None:
    blueprint = build_default_architecture()
    errors = blueprint.validate()
    if errors:
        raise SystemExit("\n".join(errors))

    print(blueprint.title)
    print("=" * len(blueprint.title))
    print("\nOrdre d'implémentation possible :")
    for item in blueprint.topological_order():
        print(f"- {item}")

    print("\nDiagramme Mermaid :")
    print(blueprint.render_mermaid())


if __name__ == "__main__":
    main()
