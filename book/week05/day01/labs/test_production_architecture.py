from pathlib import Path
import sys
import json

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_platform import (  # noqa: E402
    ArchitectureBlueprint,
    ArchitectureComponent,
    ProductionArchitectureValidator,
    ProductionControl,
    Risk,
    build_support_ai_blueprint,
    load_blueprint_from_dict,
    render_mermaid,
    summarize_readiness,
)


def assert_true(value, message):
    if not value:
        raise AssertionError(message)


def test_reference_blueprint_is_ready():
    blueprint = build_support_ai_blueprint()
    report = ProductionArchitectureValidator().validate(blueprint)
    assert_true(report.ready, report.to_json())
    assert_true(report.score >= 85, "reference blueprint should have high readiness score")


def test_missing_model_gateway_is_detected():
    blueprint = build_support_ai_blueprint()
    blueprint.components = [c for c in blueprint.components if c.kind != "model_gateway"]
    report = ProductionArchitectureValidator().validate(blueprint)
    assert_true(not report.ready, "blueprint without model gateway must not be ready")
    assert_true("model_gateway" in report.missing_components, "missing model gateway should be reported")


def test_missing_controls_are_detected():
    blueprint = build_support_ai_blueprint()
    blueprint.controls = [c for c in blueprint.controls if c.name != "cost_budget"]
    report = ProductionArchitectureValidator().validate(blueprint)
    assert_true(not report.ready, "blueprint without cost budget must not be ready")
    assert_true("cost_budget" in report.missing_controls, "missing cost budget should be reported")


def test_sensitive_actions_require_specific_controls():
    blueprint = build_support_ai_blueprint(sensitive_actions_enabled=True)
    blueprint.controls = [c for c in blueprint.controls if c.name not in {"human_approval", "audit_log"}]
    report = ProductionArchitectureValidator().validate(blueprint)
    assert_true(not report.ready, "sensitive actions without approval/audit must not be ready")
    assert_true(any("sensitive actions enabled" in w for w in report.warnings), "warning should mention sensitive actions")


def test_duplicate_components_are_rejected():
    component = ArchitectureComponent("api", "api")
    try:
        ArchitectureBlueprint(name="bad", components=[component, component], controls=[], risks=[])
    except ValueError as exc:
        assert_true("unique" in str(exc), "error should mention uniqueness")
        return
    raise AssertionError("duplicate component names should fail")


def test_component_validates_empty_name():
    try:
        ArchitectureComponent("", "api")
    except ValueError as exc:
        assert_true("name" in str(exc), "error should mention name")
        return
    raise AssertionError("empty component name should fail")


def test_duplicate_dependencies_are_rejected():
    try:
        ArchitectureComponent("runtime", "agent_runtime", dependencies=("model_gateway", "model_gateway"))
    except ValueError as exc:
        assert_true("duplicate" in str(exc), "error should mention duplicate dependencies")
        return
    raise AssertionError("duplicate dependencies should fail")


def test_mermaid_contains_edges():
    blueprint = build_support_ai_blueprint()
    mermaid = render_mermaid(blueprint)
    assert_true("flowchart LR" in mermaid, "mermaid should be a flowchart")
    assert_true("agent_runtime --> model_gateway" in mermaid, "runtime should depend on model gateway")


def test_summary_contains_status():
    report = ProductionArchitectureValidator().validate(build_support_ai_blueprint())
    summary = summarize_readiness(report)
    assert_true("Production readiness" in summary, "summary should include status")
    assert_true("Score:" in summary, "summary should include score")


def test_to_json_roundtrip_has_core_fields():
    blueprint = build_support_ai_blueprint()
    data = json.loads(blueprint.to_json())
    assert_true(data["name"] == "support-ai-production", "blueprint JSON should preserve name")
    assert_true(len(data["components"]) >= 10, "blueprint JSON should include components")
    assert_true(len(data["controls"]) >= 12, "blueprint JSON should include controls")


def test_load_simplified_blueprint_from_dict():
    data = {
        "name": "minimal",
        "components": [
            {"name": "api", "kind": "api", "critical": True},
            {"name": "security", "kind": "security", "critical": True},
            {"name": "app", "kind": "application_service", "critical": True},
            {"name": "runtime", "kind": "agent_runtime", "critical": True},
            {"name": "model", "kind": "model_gateway", "critical": True},
            {"name": "tools", "kind": "tool_gateway", "critical": True},
            {"name": "state", "kind": "state_store", "critical": True},
            {"name": "memory", "kind": "memory_store", "critical": True},
            {"name": "db", "kind": "business_database", "critical": True},
            {"name": "obs", "kind": "observability", "critical": True},
        ],
        "controls": [
            "authentication", "authorization", "rate_limiting", "timeouts",
            "bounded_retries", "structured_outputs", "tool_argument_validation",
            "pii_redaction", "cost_budget", "iteration_limit", "trace_export",
            "rollback_plan"
        ],
        "risks": ["hallucination", "tool_misuse", "pii_leakage", "cost_spike"],
    }
    blueprint = load_blueprint_from_dict(data)
    report = ProductionArchitectureValidator().validate(blueprint)
    assert_true(report.ready, report.to_json())


def test_unknown_dependency_creates_warning():
    blueprint = build_support_ai_blueprint()
    blueprint.components.append(ArchitectureComponent("bad_component", "queue", dependencies=("missing",)))
    report = ProductionArchitectureValidator().validate(blueprint)
    assert_true(any("unknown component" in warning for warning in report.warnings), "unknown dependency should warn")


def test_model_policy_warning():
    blueprint = build_support_ai_blueprint()
    blueprint.model_version_policy = "latest"
    report = ProductionArchitectureValidator().validate(blueprint)
    assert_true(any("model version" in warning for warning in report.warnings), "loose model policy should warn")


def test_prompt_policy_warning():
    blueprint = build_support_ai_blueprint()
    blueprint.prompt_version_policy = "implicit"
    report = ProductionArchitectureValidator().validate(blueprint)
    assert_true(any("prompts" in warning for warning in report.warnings), "unversioned prompt policy should warn")


def test_package_public_api_exports_core_symbols():
    import ai_platform
    expected = {
        "ArchitectureBlueprint", "ArchitectureComponent",
        "ProductionArchitectureValidator", "build_support_ai_blueprint",
        "render_mermaid",
    }
    assert_true(expected.issubset(set(ai_platform.__all__)), "public API should expose architecture symbols")


def run_all_tests():
    tests = [
        test_reference_blueprint_is_ready,
        test_missing_model_gateway_is_detected,
        test_missing_controls_are_detected,
        test_sensitive_actions_require_specific_controls,
        test_duplicate_components_are_rejected,
        test_component_validates_empty_name,
        test_duplicate_dependencies_are_rejected,
        test_mermaid_contains_edges,
        test_summary_contains_status,
        test_to_json_roundtrip_has_core_fields,
        test_load_simplified_blueprint_from_dict,
        test_unknown_dependency_creates_warning,
        test_model_policy_warning,
        test_prompt_policy_warning,
        test_package_public_api_exports_core_symbols,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")


if __name__ == "__main__":
    run_all_tests()
