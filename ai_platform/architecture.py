"""
Production architecture primitives for the AI Engineering Bootcamp.

Dependency-free module used by Week 5 Day 1.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set
import json


REQUIRED_COMPONENT_KINDS: Set[str] = {
    "api", "security", "application_service", "agent_runtime",
    "model_gateway", "tool_gateway", "state_store", "memory_store",
    "business_database", "observability",
}

REQUIRED_CONTROLS: Set[str] = {
    "authentication", "authorization", "rate_limiting", "timeouts",
    "bounded_retries", "structured_outputs", "tool_argument_validation",
    "pii_redaction", "cost_budget", "iteration_limit", "trace_export",
    "rollback_plan",
}

SENSITIVE_ACTION_CONTROLS: Set[str] = {"human_approval", "idempotency_key", "audit_log"}
REQUIRED_RISKS: Set[str] = {"hallucination", "tool_misuse", "pii_leakage", "cost_spike"}


@dataclass(frozen=True)
class ArchitectureComponent:
    """A component in a production AI platform blueprint."""

    name: str
    kind: str
    critical: bool = True
    responsibilities: Sequence[str] = field(default_factory=tuple)
    dependencies: Sequence[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("component name must not be empty")
        if not self.kind.strip():
            raise ValueError("component kind must not be empty")
        if len(set(self.dependencies)) != len(tuple(self.dependencies)):
            raise ValueError(f"component {self.name!r} has duplicate dependencies")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "kind": self.kind,
            "critical": self.critical,
            "responsibilities": list(self.responsibilities),
            "dependencies": list(self.dependencies),
        }


@dataclass(frozen=True)
class ProductionControl:
    """A production control that mitigates a class of risks."""

    name: str
    category: str
    description: str
    mandatory: bool = True

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("control name must not be empty")
        if not self.category.strip():
            raise ValueError("control category must not be empty")


@dataclass(frozen=True)
class Risk:
    """A production risk and expected mitigations."""

    name: str
    impact: str
    mitigations: Sequence[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("risk name must not be empty")
        if not self.impact.strip():
            raise ValueError("risk impact must not be empty")


@dataclass
class ArchitectureBlueprint:
    """A complete production architecture blueprint."""

    name: str
    components: List[ArchitectureComponent]
    controls: List[ProductionControl]
    risks: List[Risk]
    sensitive_actions_enabled: bool = False
    model_version_policy: str = "pinned_or_evaluated"
    prompt_version_policy: str = "versioned"
    schema_version_policy: str = "versioned"
    deployment_strategy: str = "progressive_rollout"

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("blueprint name must not be empty")
        names = [component.name for component in self.components]
        if len(names) != len(set(names)):
            raise ValueError("component names must be unique")
        control_names = [control.name for control in self.controls]
        if len(control_names) != len(set(control_names)):
            raise ValueError("control names must be unique")
        risk_names = [risk.name for risk in self.risks]
        if len(risk_names) != len(set(risk_names)):
            raise ValueError("risk names must be unique")

    @property
    def component_kinds(self) -> Set[str]:
        return {component.kind for component in self.components}

    @property
    def control_names(self) -> Set[str]:
        return {control.name for control in self.controls}

    @property
    def risk_names(self) -> Set[str]:
        return {risk.name for risk in self.risks}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "components": [component.to_dict() for component in self.components],
            "controls": [asdict(control) for control in self.controls],
            "risks": [asdict(risk) for risk in self.risks],
            "sensitive_actions_enabled": self.sensitive_actions_enabled,
            "model_version_policy": self.model_version_policy,
            "prompt_version_policy": self.prompt_version_policy,
            "schema_version_policy": self.schema_version_policy,
            "deployment_strategy": self.deployment_strategy,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


@dataclass(frozen=True)
class ReadinessReport:
    """Validation output for a production architecture."""

    ready: bool
    score: int
    missing_components: List[str]
    missing_controls: List[str]
    missing_risks: List[str]
    warnings: List[str]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


class ProductionArchitectureValidator:
    """Validate whether an AI platform architecture is production-ready."""

    def __init__(
        self,
        required_components: Optional[Iterable[str]] = None,
        required_controls: Optional[Iterable[str]] = None,
        required_risks: Optional[Iterable[str]] = None,
    ) -> None:
        self.required_components = set(required_components or REQUIRED_COMPONENT_KINDS)
        self.required_controls = set(required_controls or REQUIRED_CONTROLS)
        self.required_risks = set(required_risks or REQUIRED_RISKS)

    def validate(self, blueprint: ArchitectureBlueprint) -> ReadinessReport:
        missing_components = sorted(self.required_components - blueprint.component_kinds)
        missing_controls = sorted(self.required_controls - blueprint.control_names)
        missing_risks = sorted(self.required_risks - blueprint.risk_names)
        warnings: List[str] = []
        recommendations: List[str] = []

        if blueprint.sensitive_actions_enabled:
            missing_sensitive = sorted(SENSITIVE_ACTION_CONTROLS - blueprint.control_names)
            if missing_sensitive:
                warnings.append("sensitive actions enabled without controls: " + ", ".join(missing_sensitive))
                recommendations.append("Require human approval, idempotency keys and audit logs for sensitive tools.")

        if blueprint.model_version_policy not in {"pinned", "pinned_or_evaluated"}:
            warnings.append("model version policy is not strict enough")
            recommendations.append("Pin model versions or gate upgrades with evals.")
        if blueprint.prompt_version_policy != "versioned":
            warnings.append("prompts are not explicitly versioned")
            recommendations.append("Version prompts like application code.")
        if blueprint.schema_version_policy != "versioned":
            warnings.append("schemas are not explicitly versioned")
            recommendations.append("Version structured output and tool schemas.")
        if blueprint.deployment_strategy not in {"blue_green", "canary", "progressive_rollout"}:
            warnings.append("deployment strategy does not support progressive rollback")
            recommendations.append("Use canary, blue-green or progressive rollout.")

        component_names = {component.name for component in blueprint.components}
        for component in blueprint.components:
            for dependency in component.dependencies:
                if dependency not in component_names:
                    warnings.append(f"component {component.name!r} depends on unknown component {dependency!r}")

        score = self._score(missing_components, missing_controls, missing_risks, warnings)
        ready = (
            not missing_components
            and not missing_controls
            and not missing_risks
            and not any("sensitive actions enabled" in warning for warning in warnings)
            and score >= 85
        )

        if missing_components:
            recommendations.append("Add missing critical components: " + ", ".join(missing_components))
        if missing_controls:
            recommendations.append("Add missing controls: " + ", ".join(missing_controls))
        if missing_risks:
            recommendations.append("Document missing risks: " + ", ".join(missing_risks))

        return ReadinessReport(
            ready=ready,
            score=score,
            missing_components=missing_components,
            missing_controls=missing_controls,
            missing_risks=missing_risks,
            warnings=warnings,
            recommendations=recommendations,
        )

    @staticmethod
    def _score(
        missing_components: Sequence[str],
        missing_controls: Sequence[str],
        missing_risks: Sequence[str],
        warnings: Sequence[str],
    ) -> int:
        score = 100
        score -= len(missing_components) * 8
        score -= len(missing_controls) * 4
        score -= len(missing_risks) * 3
        score -= len(warnings) * 2
        return max(0, min(100, score))


def build_support_ai_blueprint(sensitive_actions_enabled: bool = True) -> ArchitectureBlueprint:
    """Build the reference production architecture for the lab."""

    components = [
        ArchitectureComponent("backend_api", "api", responsibilities=("HTTP contract", "input validation", "response mapping"), dependencies=("auth_rate_limit", "support_service")),
        ArchitectureComponent("auth_rate_limit", "security", responsibilities=("authentication", "authorization", "rate limiting")),
        ArchitectureComponent("support_service", "application_service", responsibilities=("business use case", "context loading", "runtime invocation"), dependencies=("agent_runtime", "business_db", "observability")),
        ArchitectureComponent("agent_runtime", "agent_runtime", responsibilities=("bounded agent loop", "guardrails", "structured outputs"), dependencies=("model_gateway", "tool_gateway", "state_store", "memory_store", "observability")),
        ArchitectureComponent("model_gateway", "model_gateway", responsibilities=("timeouts", "bounded retries", "model version policy", "cost tracking")),
        ArchitectureComponent("tool_gateway", "tool_gateway", responsibilities=("tool validation", "permission checks", "human approval"), dependencies=("human_approval", "observability")),
        ArchitectureComponent("state_store", "state_store", responsibilities=("session isolation", "conversation slots", "runtime status")),
        ArchitectureComponent("memory_store", "memory_store", responsibilities=("durable preferences", "forget user", "visibility policy")),
        ArchitectureComponent("business_db", "business_database", responsibilities=("tickets", "orders", "refunds", "users")),
        ArchitectureComponent("observability", "observability", responsibilities=("traces", "metrics", "logs", "redaction", "health reports")),
        ArchitectureComponent("human_approval", "human_approval", responsibilities=("approve sensitive actions", "audit decision")),
    ]

    controls = [
        ProductionControl("authentication", "security", "Verify caller identity."),
        ProductionControl("authorization", "security", "Check user and tool permissions."),
        ProductionControl("rate_limiting", "reliability", "Limit request volume."),
        ProductionControl("timeouts", "reliability", "Bound external calls."),
        ProductionControl("bounded_retries", "reliability", "Retry transient failures without loops."),
        ProductionControl("structured_outputs", "quality", "Validate model outputs."),
        ProductionControl("tool_argument_validation", "security", "Validate tool call arguments."),
        ProductionControl("pii_redaction", "data", "Remove sensitive data from logs."),
        ProductionControl("cost_budget", "cost", "Limit spend per request and user."),
        ProductionControl("iteration_limit", "cost", "Bound agent steps."),
        ProductionControl("trace_export", "observability", "Export traces and key spans."),
        ProductionControl("rollback_plan", "delivery", "Restore known good versions."),
        ProductionControl("human_approval", "security", "Require approval for sensitive actions."),
        ProductionControl("idempotency_key", "reliability", "Prevent duplicate side effects."),
        ProductionControl("audit_log", "security", "Record sensitive decisions."),
    ]

    risks = [
        Risk("hallucination", "Incorrect answer sent to user.", ("structured_outputs", "trace_export")),
        Risk("tool_misuse", "Incorrect external action.", ("tool_argument_validation", "human_approval")),
        Risk("pii_leakage", "Sensitive data appears in logs or prompts.", ("pii_redaction",)),
        Risk("cost_spike", "Unexpected spend from loops or large context.", ("cost_budget", "iteration_limit")),
        Risk("latency_spike", "Bad user experience.", ("timeouts", "bounded_retries")),
        Risk("state_corruption", "Wrong state reused across users.", ("authorization", "trace_export")),
    ]

    return ArchitectureBlueprint(
        name="support-ai-production",
        components=components,
        controls=controls,
        risks=risks,
        sensitive_actions_enabled=sensitive_actions_enabled,
        model_version_policy="pinned_or_evaluated",
        prompt_version_policy="versioned",
        schema_version_policy="versioned",
        deployment_strategy="progressive_rollout",
    )


def render_mermaid(blueprint: ArchitectureBlueprint) -> str:
    """Render a simple Mermaid flowchart from component dependencies."""

    lines = ["flowchart LR"]
    for component in blueprint.components:
        lines.append(f"    {component.name}[{component.name}\\n{component.kind}]")
    for component in blueprint.components:
        for dependency in component.dependencies:
            lines.append(f"    {component.name} --> {dependency}")
    return "\n".join(lines)


def summarize_readiness(report: ReadinessReport) -> str:
    """Create a human-readable readiness summary."""

    status = "READY" if report.ready else "NOT READY"
    lines = [f"Production readiness: {status}", f"Score: {report.score}/100"]
    if report.missing_components:
        lines.append("Missing components: " + ", ".join(report.missing_components))
    if report.missing_controls:
        lines.append("Missing controls: " + ", ".join(report.missing_controls))
    if report.missing_risks:
        lines.append("Missing risks: " + ", ".join(report.missing_risks))
    if report.warnings:
        lines.append("Warnings: " + " | ".join(report.warnings))
    return "\n".join(lines)


def load_blueprint_from_dict(data: Dict[str, Any]) -> ArchitectureBlueprint:
    """Load a blueprint from a dictionary."""

    components = [
        ArchitectureComponent(
            name=item["name"],
            kind=item["kind"],
            critical=bool(item.get("critical", True)),
            responsibilities=tuple(item.get("responsibilities", ())),
            dependencies=tuple(item.get("dependencies", ())),
        )
        for item in data["components"]
    ]
    controls = [
        ProductionControl(
            name=item["name"] if isinstance(item, dict) else str(item),
            category=item.get("category", "unspecified") if isinstance(item, dict) else "unspecified",
            description=item.get("description", "") if isinstance(item, dict) else "",
            mandatory=bool(item.get("mandatory", True)) if isinstance(item, dict) else True,
        )
        for item in data["controls"]
    ]
    risks = [
        Risk(
            name=item["name"] if isinstance(item, dict) else str(item),
            impact=item.get("impact", "unspecified") if isinstance(item, dict) else "unspecified",
            mitigations=tuple(item.get("mitigations", ())) if isinstance(item, dict) else (),
        )
        for item in data["risks"]
    ]

    return ArchitectureBlueprint(
        name=data["name"],
        components=components,
        controls=controls,
        risks=risks,
        sensitive_actions_enabled=bool(data.get("sensitive_actions_enabled", False)),
        model_version_policy=data.get("model_version_policy", "pinned_or_evaluated"),
        prompt_version_policy=data.get("prompt_version_policy", "versioned"),
        schema_version_policy=data.get("schema_version_policy", "versioned"),
        deployment_strategy=data.get("deployment_strategy", "progressive_rollout"),
    )


if __name__ == "__main__":
    blueprint = build_support_ai_blueprint()
    report = ProductionArchitectureValidator().validate(blueprint)
    print(summarize_readiness(report))
    print()
    print(render_mermaid(blueprint))
