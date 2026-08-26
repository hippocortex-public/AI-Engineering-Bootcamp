from mini_framework_architecture import (
    ArchitectureBlueprint,
    ComponentSpec,
    DecisionRecord,
    build_default_architecture,
)


def assert_true(value, message):
    if not value:
        raise AssertionError(message)


def test_default_blueprint_is_valid():
    blueprint = build_default_architecture()
    assert_true(blueprint.validate() == [], "default blueprint should be valid")


def test_required_components_exist():
    blueprint = build_default_architecture()
    names = blueprint.component_names()
    for name in {
        "agent_definition",
        "runner",
        "model_client",
        "tool_registry",
        "memory_store",
        "workflow_engine",
        "observability",
    }:
        assert_true(name in names, f"missing component: {name}")


def test_duplicate_component_is_rejected():
    blueprint = build_default_architecture()
    duplicated = ArchitectureBlueprint(
        title=blueprint.title,
        objective=blueprint.objective,
        components=blueprint.components + [blueprint.components[0]],
        decisions=blueprint.decisions,
        invariants=blueprint.invariants,
    )
    errors = duplicated.validate()
    assert_true(any("duplicate component" in error for error in errors), errors)


def test_unknown_dependency_is_rejected():
    blueprint = build_default_architecture()
    broken_component = ComponentSpec(
        name="broken",
        responsibility="Composant mal câblé.",
        interfaces=("run",),
        depends_on=("missing",),
    )
    broken = ArchitectureBlueprint(
        title=blueprint.title,
        objective=blueprint.objective,
        components=blueprint.components + [broken_component],
        decisions=blueprint.decisions,
        invariants=blueprint.invariants,
    )
    errors = broken.validate()
    assert_true(any("unknown dependency" in error for error in errors), errors)


def test_cycle_is_rejected():
    components = [
        ComponentSpec("agent_definition", "A", ("x",), ("runner",)),
        ComponentSpec("runner", "B", ("x",), ("agent_definition",)),
        ComponentSpec("model_client", "C", ("x",), ()),
        ComponentSpec("tool_registry", "D", ("x",), ()),
        ComponentSpec("memory_store", "E", ("x",), ()),
        ComponentSpec("workflow_engine", "F", ("x",), ()),
        ComponentSpec("observability", "G", ("x",), ()),
    ]
    blueprint = ArchitectureBlueprint(
        title="Cycle",
        objective="Tester un cycle.",
        components=components,
        decisions=[DecisionRecord("ADR-X", "Décision", "Raison", "Tradeoff")],
        invariants=["A", "B", "C"],
    )
    errors = blueprint.validate()
    assert_true(any("cyclic dependency" in error for error in errors), errors)


def test_topological_order_places_dependencies_first():
    blueprint = build_default_architecture()
    order = blueprint.topological_order()
    runner_index = order.index("runner")
    assert_true(order.index("agent_definition") < runner_index, order)
    assert_true(order.index("model_client") < runner_index, order)
    assert_true(order.index("tool_registry") < runner_index, order)


def test_mermaid_contains_expected_edges():
    mermaid = build_default_architecture().render_mermaid()
    assert_true("flowchart TD" in mermaid, mermaid)
    assert_true("runner --> model_client" in mermaid, mermaid)
    assert_true("runner --> tool_registry" in mermaid, mermaid)


def test_json_roundtrip_keeps_components():
    blueprint = build_default_architecture()
    restored = ArchitectureBlueprint.from_json(blueprint.to_json())
    assert_true(restored.component_names() == blueprint.component_names(), "roundtrip mismatch")
    assert_true(restored.validate() == [], restored.validate())


def test_decisions_are_documented_with_reason_and_tradeoff():
    blueprint = build_default_architecture()
    for decision in blueprint.decisions:
        assert_true(decision.reason, "reason required")
        assert_true(decision.tradeoff, "tradeoff required")


def test_extension_with_adapter_remains_valid():
    blueprint = build_default_architecture()
    mcp_adapter = ComponentSpec(
        name="mcp_tool_adapter",
        responsibility="Adapte des outils MCP au contrat du ToolRegistry.",
        interfaces=("list_tools", "call_tool"),
        depends_on=("tool_registry",),
        risks=("couplage protocolaire",),
    )
    extended = ArchitectureBlueprint(
        title=blueprint.title,
        objective=blueprint.objective,
        components=blueprint.components + [mcp_adapter],
        decisions=blueprint.decisions,
        invariants=blueprint.invariants,
    )
    assert_true(extended.validate() == [], extended.validate())


def test_specialized_components_do_not_depend_on_runner():
    blueprint = build_default_architecture()
    for component in blueprint.components:
        if component.name not in {"application"}:
            assert_true(
                "runner" not in component.depends_on,
                f"{component.name} should not depend on runner",
            )


def test_implementation_plan_prepares_week_progression():
    plan = build_default_architecture().implementation_plan()
    expected = ["Jour 2", "Jour 3", "Jour 4", "Jour 5", "Jour 6", "Jour 7"]
    for marker in expected:
        assert_true(any(marker in item for item in plan), f"missing {marker}")


def test_component_without_interface_is_invalid():
    component = ComponentSpec(
        name="bad_component",
        responsibility="Responsabilité déclarée.",
        interfaces=(),
        depends_on=(),
    )
    errors = component.validate()
    assert_true(any("interface" in error for error in errors), errors)


def run_all_tests():
    tests = [
        test_default_blueprint_is_valid,
        test_required_components_exist,
        test_duplicate_component_is_rejected,
        test_unknown_dependency_is_rejected,
        test_cycle_is_rejected,
        test_topological_order_places_dependencies_first,
        test_mermaid_contains_expected_edges,
        test_json_roundtrip_keeps_components,
        test_decisions_are_documented_with_reason_and_tradeoff,
        test_extension_with_adapter_remains_valid,
        test_specialized_components_do_not_depend_on_runner,
        test_implementation_plan_prepares_week_progression,
        test_component_without_interface_is_invalid,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")


if __name__ == "__main__":
    run_all_tests()
