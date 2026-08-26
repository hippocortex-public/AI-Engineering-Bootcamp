from autonomous_agent import (
    AgentState,
    AutonomousSupportAgent,
    RunStatus,
    TaskStatus,
    ToolRegistry,
    ToolDefinition,
    ToolResult,
    build_default_registry,
    extract_order_id,
)


def make_agent():
    return AutonomousSupportAgent(build_default_registry())


def test_extract_order_id():
    assert extract_order_id("remboursement order-1234") == "ORDER-1234"
    assert extract_order_id("commande cmd-2024") == "CMD-2024"
    assert extract_order_id("pas de commande") is None


def test_refund_plan_requires_order_id():
    state = make_agent().start("u1", "Je veux un remboursement")
    assert state.status == RunStatus.NEEDS_INPUT
    assert "order_id" in state.missing_inputs
    assert state.tasks == []


def test_refund_plan_contains_expected_tasks():
    state = make_agent().start("u1", "Je veux un remboursement pour ORDER-1234")
    assert state.status == RunStatus.RUNNING
    assert [task.tool_name for task in state.tasks] == [
        "search_refund_policy",
        "check_order",
        "create_support_ticket",
        "issue_refund",
        "draft_response",
    ]


def test_agent_stops_for_sensitive_action_without_approval():
    agent = make_agent()
    state = agent.start("u1", "Je veux un remboursement pour ORDER-1234")
    final_state = agent.run(state, approve_sensitive_actions=False)
    assert final_state.status == RunStatus.NEEDS_INPUT
    assert "approval_for_issue_refund" in final_state.missing_inputs
    assert any(task.tool_name == "issue_refund" and task.status == TaskStatus.BLOCKED for task in final_state.tasks)


def test_agent_completes_with_approval():
    agent = make_agent()
    state = agent.start("u1", "Je veux un remboursement pour ORDER-1234")
    final_state = agent.run(state, approve_sensitive_actions=True)
    assert final_state.status == RunStatus.COMPLETED
    assert final_state.final_answer is not None
    assert "ORDER-1234" in final_state.final_answer
    assert any(task.tool_name == "issue_refund" and task.status == TaskStatus.DONE for task in final_state.tasks)


def test_agent_respects_max_steps_guardrail():
    agent = make_agent()
    state = agent.start("u1", "Je veux un remboursement pour ORDER-1234")
    final_state = agent.run(state, max_steps=1, approve_sensitive_actions=True)
    assert final_state.status == RunStatus.STOPPED
    assert final_state.current_step == 1


def test_agent_respects_budget_guardrail():
    agent = make_agent()
    state = agent.start("u1", "Je veux un remboursement pour ORDER-1234", max_budget=1)
    final_state = agent.run(state, approve_sensitive_actions=True)
    assert final_state.status == RunStatus.STOPPED
    assert any(event.event_type == "budget_exceeded" for event in final_state.traces)


def test_state_serialization_roundtrip():
    agent = make_agent()
    state = agent.start("u1", "Créer un ticket support")
    restored = AgentState.from_json(state.to_json())
    assert restored.user_id == "u1"
    assert restored.objective == state.objective
    assert len(restored.tasks) == len(state.tasks)


def test_unknown_tool_is_rejected():
    registry = ToolRegistry()
    registry.register(ToolDefinition("known_tool", "Known", lambda args: ToolResult(ok=True, data={})))
    try:
        registry.execute("missing_tool", {})
        assert False, "Expected KeyError"
    except KeyError as exc:
        assert "Unknown tool" in str(exc)


def test_trace_contains_plan_and_task_events():
    agent = make_agent()
    state = agent.start("u1", "Créer un ticket support")
    final_state = agent.run(state)
    event_types = [event.event_type for event in final_state.traces]
    assert "plan_created" in event_types
    assert "task_started" in event_types
    assert "task_completed" in event_types
    assert final_state.status == RunStatus.COMPLETED


if __name__ == "__main__":
    tests = [
        test_extract_order_id,
        test_refund_plan_requires_order_id,
        test_refund_plan_contains_expected_tasks,
        test_agent_stops_for_sensitive_action_without_approval,
        test_agent_completes_with_approval,
        test_agent_respects_max_steps_guardrail,
        test_agent_respects_budget_guardrail,
        test_state_serialization_roundtrip,
        test_unknown_tool_is_rejected,
        test_trace_contains_plan_and_task_events,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
