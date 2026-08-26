"""Tests for the integrated mini-framework lab."""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mini_framework.integration import (
    AgentSpec,
    ApprovalRequired,
    MiniAgentFramework,
    PermissionError,
    ToolSpec,
    ToolRegistry,
    ValidationError,
    WorkflowDefinition,
    WorkflowStep,
    build_support_framework,
)


def assert_raises(exc_type, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except exc_type:
        return
    raise AssertionError(f"Expected {exc_type.__name__}")


def test_agent_validation_requires_name():
    agent = AgentSpec(name="", instructions="x", allowed_tools=[])
    assert_raises(ValidationError, agent.validate)


def test_agent_validation_rejects_duplicate_tools():
    agent = AgentSpec(name="a", instructions="x", allowed_tools=["t", "t"])
    assert_raises(ValidationError, agent.validate)


def test_tool_registry_registers_tools():
    registry = ToolRegistry()
    registry.register(
        ToolSpec(
            name="echo",
            description="Echo input.",
            input_schema={
                "type": "object",
                "required": ["text"],
                "properties": {"text": {"type": "string"}},
                "additionalProperties": False,
            },
            handler=lambda args: {"text": args["text"]},
        )
    )
    assert registry.list_tools() == ["echo"]


def test_tool_validation_rejects_missing_argument():
    framework = build_support_framework()
    agent = framework.agents["support_agent"]
    assert_raises(
        ValidationError,
        framework.tools.call,
        tool_name="classify_ticket",
        arguments={},
        agent=agent,
    )


def test_tool_validation_rejects_unexpected_argument():
    framework = build_support_framework()
    agent = framework.agents["support_agent"]
    assert_raises(
        ValidationError,
        framework.tools.call,
        tool_name="classify_ticket",
        arguments={"message": "hello", "extra": "no"},
        agent=agent,
    )


def test_tool_permission_is_enforced():
    framework = build_support_framework()
    restricted = AgentSpec(
        name="restricted",
        instructions="Can only classify.",
        allowed_tools=["classify_ticket"],
    )
    framework.register_agent(restricted)
    assert_raises(
        PermissionError,
        framework.tools.call,
        tool_name="draft_answer",
        arguments={"message": "x", "memory": {}, "outputs": {}},
        agent=restricted,
    )


def test_sensitive_tool_requires_approval():
    framework = build_support_framework()
    agent = framework.agents["support_agent"]
    assert_raises(
        ApprovalRequired,
        framework.tools.call,
        tool_name="issue_refund",
        arguments={"amount": 42},
        agent=agent,
        approval=False,
    )


def test_sensitive_tool_runs_with_approval():
    framework = build_support_framework()
    agent = framework.agents["support_agent"]
    result = framework.tools.call(
        tool_name="issue_refund",
        arguments={"amount": 42},
        agent=agent,
        approval=True,
    )
    assert result.ok is True
    assert result.data["refund_prepared"] is True


def test_memory_is_user_scoped():
    framework = build_support_framework()
    framework.memory.remember("u1", "preferred_tone", "calme")
    assert framework.memory.retrieve("u1") == {"preferred_tone": "calme"}
    assert framework.memory.retrieve("u2") == {}


def test_workflow_cycle_is_rejected():
    workflow = WorkflowDefinition(
        name="bad",
        steps=[
            WorkflowStep(name="a", agent_name="x", tool_name="t", depends_on=["b"]),
            WorkflowStep(name="b", agent_name="x", tool_name="t", depends_on=["a"]),
        ],
    )
    assert_raises(ValidationError, workflow.validate)


def test_workflow_unknown_dependency_is_rejected():
    workflow = WorkflowDefinition(
        name="bad",
        steps=[
            WorkflowStep(name="a", agent_name="x", tool_name="t", depends_on=["missing"]),
        ],
    )
    assert_raises(ValidationError, workflow.validate)


def test_support_workflow_completes():
    framework = build_support_framework()
    result = framework.run(
        user_id="u1",
        message="Ma commande est cassée.",
        workflow_name="support_resolution",
    )
    assert result.status == "completed"
    assert "classify" in result.outputs
    assert "search_policy" in result.outputs
    assert "draft" in result.outputs


def test_support_workflow_uses_memory():
    framework = build_support_framework()
    framework.memory.remember("u1", "preferred_tone", "empathique")
    result = framework.run(
        user_id="u1",
        message="Je veux un remboursement.",
        workflow_name="support_resolution",
    )
    assert result.status == "completed"
    assert result.memory_used == ["preferred_tone"]
    assert "empathique" in result.outputs["draft"]["draft"]


def test_refund_workflow_blocks_without_approval():
    framework = build_support_framework()
    result = framework.run(
        user_id="u1",
        message="Je veux un remboursement.",
        workflow_name="support_refund_with_approval",
        approval=False,
    )
    assert result.status == "blocked"
    assert result.blocked_actions == ["issue_refund"]


def test_refund_workflow_runs_with_approval_when_amount_in_context_missing_fails_cleanly():
    framework = build_support_framework()
    result = framework.run(
        user_id="u1",
        message="Je veux un remboursement.",
        workflow_name="support_refund_with_approval",
        approval=True,
    )
    assert result.status == "failed"
    assert "amount" in result.summary or "number" in result.summary


def test_unknown_workflow_fails_cleanly():
    framework = build_support_framework()
    result = framework.run(
        user_id="u1",
        message="hello",
        workflow_name="missing",
    )
    assert result.status == "failed"
    assert "Unknown workflow" in result.summary


def test_unknown_agent_fails_cleanly():
    framework = build_support_framework()
    framework.register_workflow(
        WorkflowDefinition(
            name="unknown_agent_workflow",
            steps=[
                WorkflowStep(name="x", agent_name="ghost", tool_name="classify_ticket", argument_keys=["message"])
            ],
        )
    )
    result = framework.run(
        user_id="u1",
        message="hello",
        workflow_name="unknown_agent_workflow",
    )
    assert result.status == "failed"
    assert "Unknown agent" in result.summary


def test_trace_contains_core_events():
    framework = build_support_framework()
    result = framework.run(
        user_id="u1",
        message="Ma commande est cassée.",
        workflow_name="support_resolution",
    )
    names = [event["name"] for event in result.trace]
    assert "run.started" in names
    assert "memory.retrieved" in names
    assert "tool.call.started" in names
    assert "run.completed" in names


def test_run_result_is_json_serializable():
    framework = build_support_framework()
    result = framework.run(
        user_id="u1",
        message="Ma commande est cassée.",
        workflow_name="support_resolution",
    )
    payload = json.loads(result.to_json())
    assert payload["status"] == "completed"
    assert isinstance(payload["trace"], list)


def test_memory_forget_removes_key():
    framework = build_support_framework()
    framework.memory.remember("u1", "preferred_tone", "direct")
    framework.memory.forget("u1", "preferred_tone")
    assert framework.memory.retrieve("u1") == {}


if __name__ == "__main__":
    tests = [
        test_agent_validation_requires_name,
        test_agent_validation_rejects_duplicate_tools,
        test_tool_registry_registers_tools,
        test_tool_validation_rejects_missing_argument,
        test_tool_validation_rejects_unexpected_argument,
        test_tool_permission_is_enforced,
        test_sensitive_tool_requires_approval,
        test_sensitive_tool_runs_with_approval,
        test_memory_is_user_scoped,
        test_workflow_cycle_is_rejected,
        test_workflow_unknown_dependency_is_rejected,
        test_support_workflow_completes,
        test_support_workflow_uses_memory,
        test_refund_workflow_blocks_without_approval,
        test_refund_workflow_runs_with_approval_when_amount_in_context_missing_fails_cleanly,
        test_unknown_workflow_fails_cleanly,
        test_unknown_agent_fails_cleanly,
        test_trace_contains_core_events,
        test_run_result_is_json_serializable,
        test_memory_forget_removes_key,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
