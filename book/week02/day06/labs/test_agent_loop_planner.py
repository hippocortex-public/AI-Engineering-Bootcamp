"""
Tests du lab Jour 6 — Agent Loop & planification.

Ces tests utilisent uniquement la bibliothèque standard.
"""

from agent_loop_planner import (
    AgentLoop,
    ToolAction,
    ToolRegistry,
    build_default_registry,
    extract_order_id,
)


def test_extract_order_id_detects_valid_id():
    assert extract_order_id("Ma commande A-100 est en retard") == "A-100"


def test_extract_order_id_returns_none_when_missing():
    assert extract_order_id("Ma commande est en retard") is None


def test_registry_refuses_unknown_tool():
    registry = ToolRegistry()
    observation = registry.execute(ToolAction("unknown_tool", {}))

    assert observation.success is False
    assert observation.error == "Unknown tool: unknown_tool"


def test_nominal_agent_loop_completes():
    loop = AgentLoop(build_default_registry(), max_iterations=5)

    state = loop.run("Bonjour, ma commande A-100 est en retard. Pouvez-vous m'aider ?")

    assert state.status == "completed"
    assert state.order_id == "A-100"
    assert state.order_status == "delayed"
    assert state.eta == "2026-09-02"
    assert state.final_answer is not None
    assert "A-100" in state.final_answer
    assert len(state.trace) == 2


def test_agent_asks_clarification_when_order_id_is_missing():
    loop = AgentLoop(build_default_registry(), max_iterations=5)

    state = loop.run("Bonjour, ma commande est en retard.")

    assert state.status == "waiting_for_user"
    assert state.final_answer == "Pouvez-vous me transmettre votre identifiant de commande ?"
    assert state.trace[0]["action"] == "ask_clarification"


def test_agent_records_trace_fields():
    loop = AgentLoop(build_default_registry(), max_iterations=5)

    state = loop.run("Commande A-100 en retard")

    first_trace = state.trace[0]
    assert first_trace["iteration"] == 1
    assert first_trace["action"] == "lookup_order"
    assert first_trace["success"] is True
    assert "order_status" in first_trace["updated_fields"]


def test_agent_handles_tool_error():
    loop = AgentLoop(build_default_registry(), max_iterations=5)

    state = loop.run("Commande Z-999 en retard")

    assert state.status == "error"
    assert state.trace[0]["success"] is False
    assert "not found" in state.trace[0]["error"]


def test_agent_enforces_max_iterations():
    registry = ToolRegistry()

    def incomplete_lookup_order(order_id):
        return {"order_id": order_id, "status": None, "eta": None}

    registry.register("lookup_order", incomplete_lookup_order)
    loop = AgentLoop(registry, max_iterations=1)

    state = loop.run("Commande A-100 en retard")

    assert state.status == "max_iterations_reached"
    assert state.iterations == 1


def test_state_serializes_to_json():
    loop = AgentLoop(build_default_registry(), max_iterations=5)

    state = loop.run("Commande A-100 en retard")
    payload = state.to_json()

    assert '"status": "completed"' in payload
    assert '"order_id": "A-100"' in payload


def run_all_tests():
    tests = [
        test_extract_order_id_detects_valid_id,
        test_extract_order_id_returns_none_when_missing,
        test_registry_refuses_unknown_tool,
        test_nominal_agent_loop_completes,
        test_agent_asks_clarification_when_order_id_is_missing,
        test_agent_records_trace_fields,
        test_agent_handles_tool_error,
        test_agent_enforces_max_iterations,
        test_state_serializes_to_json,
    ]

    for test in tests:
        test()

    print(f"{len(tests)} tests passed")


if __name__ == "__main__":
    run_all_tests()
