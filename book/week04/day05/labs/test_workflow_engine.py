from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mini_framework.workflow import (
    WorkflowDefinition,
    WorkflowEngine,
    WorkflowStep,
    WorkflowValidationError,
)
from workflow_engine_lab import build_support_workflow, register_support_handlers


def build_engine():
    engine = WorkflowEngine()
    register_support_handlers(engine)
    return engine


def test_successful_refund_workflow():
    engine = build_engine()
    run = engine.run(
        build_support_workflow(),
        input_payload={"message": "refund please", "amount": 10},
        approvals={"refund"},
        run_id="run_success",
    )
    assert run.status == "completed"
    assert run.step_results["refund"].status == "completed"
    assert run.state.data["final_answer"]["status"] == "resolved"


def test_sensitive_step_blocks_without_approval():
    engine = build_engine()
    run = engine.run(
        build_support_workflow(),
        input_payload={"message": "refund please", "amount": 10},
        approvals=set(),
        run_id="run_blocked",
    )
    assert run.status == "blocked"
    assert run.step_results["refund"].status == "blocked"
    assert run.step_results["final_answer"].status == "skipped"


def test_non_refund_skips_refund_and_completes():
    engine = build_engine()
    run = engine.run(
        build_support_workflow(),
        input_payload={"message": "bug on login"},
        run_id="run_bug",
    )
    assert run.status == "completed"
    assert run.step_results["refund"].status == "skipped"
    assert run.step_results["final_answer"].status == "completed"


def test_retry_succeeds_after_temporary_failure():
    engine = build_engine()
    run = engine.run(
        build_support_workflow(),
        input_payload={"message": "bug", "force_plan_failure": True},
        run_id="run_retry",
    )
    assert run.status == "completed"
    assert run.step_results["plan"].attempts == 2
    assert any(event.event == "step.retry_scheduled" for event in run.trace)


def test_failed_step_skips_dependents():
    engine = build_engine()
    run = engine.run(
        build_support_workflow(),
        input_payload={"message": "refund please", "amount": 0},
        approvals={"refund"},
        run_id="run_failed",
    )
    assert run.status == "failed"
    assert run.step_results["refund"].status == "failed"
    assert run.step_results["final_answer"].status == "skipped"


def test_duplicate_step_names_rejected():
    engine = WorkflowEngine()
    engine.register_handler("noop", lambda ctx: None)
    workflow = WorkflowDefinition(
        name="bad",
        version="1",
        steps=[
            WorkflowStep(name="a", handler="noop"),
            WorkflowStep(name="a", handler="noop"),
        ],
    )
    try:
        engine.validate(workflow)
        assert False, "expected WorkflowValidationError"
    except WorkflowValidationError as exc:
        assert "duplicate" in str(exc)


def test_unknown_dependency_rejected():
    engine = WorkflowEngine()
    engine.register_handler("noop", lambda ctx: None)
    workflow = WorkflowDefinition(
        name="bad",
        version="1",
        steps=[WorkflowStep(name="a", handler="noop", depends_on=("missing",))],
    )
    try:
        engine.validate(workflow)
        assert False, "expected WorkflowValidationError"
    except WorkflowValidationError as exc:
        assert "unknown dependencies" in str(exc)


def test_cycle_rejected():
    engine = WorkflowEngine()
    engine.register_handler("noop", lambda ctx: None)
    workflow = WorkflowDefinition(
        name="bad",
        version="1",
        steps=[
            WorkflowStep(name="a", handler="noop", depends_on=("b",)),
            WorkflowStep(name="b", handler="noop", depends_on=("a",)),
        ],
    )
    try:
        engine.validate(workflow)
        assert False, "expected WorkflowValidationError"
    except WorkflowValidationError as exc:
        assert "cycle" in str(exc)


def test_missing_handler_rejected():
    engine = WorkflowEngine()
    workflow = WorkflowDefinition(
        name="bad",
        version="1",
        steps=[WorkflowStep(name="a", handler="missing")],
    )
    try:
        engine.validate(workflow)
        assert False, "expected WorkflowValidationError"
    except WorkflowValidationError as exc:
        assert "missing handler" in str(exc)


def test_missing_condition_rejected():
    engine = WorkflowEngine()
    engine.register_handler("noop", lambda ctx: None)
    workflow = WorkflowDefinition(
        name="bad",
        version="1",
        steps=[WorkflowStep(name="a", handler="noop", condition="missing")],
    )
    try:
        engine.validate(workflow)
        assert False, "expected WorkflowValidationError"
    except WorkflowValidationError as exc:
        assert "missing condition" in str(exc)


def test_manifest_contains_execution_order():
    engine = build_engine()
    manifest = engine.manifest(build_support_workflow())
    assert manifest["execution_order"][0] == "classify"
    assert "final_answer" in manifest["execution_order"]
    assert manifest["steps"][0]["handler"] == "classify_ticket"


def test_run_json_is_serializable():
    engine = build_engine()
    run = engine.run(
        build_support_workflow(),
        input_payload={"message": "hello"},
        run_id="run_json",
    )
    payload = json.loads(run.to_json())
    assert payload["run_id"] == "run_json"
    assert isinstance(payload["trace"], list)


def test_state_records_step_outputs():
    engine = build_engine()
    run = engine.run(
        build_support_workflow(),
        input_payload={"message": "general question"},
        run_id="run_state",
    )
    assert "classify" in run.state.data
    assert "plan" in run.state.data
    assert run.state.status == "completed"


def test_trace_contains_workflow_boundaries():
    engine = build_engine()
    run = engine.run(
        build_support_workflow(),
        input_payload={"message": "hello"},
        run_id="run_trace",
    )
    assert run.trace[0].event == "workflow.started"
    assert run.trace[-1].event == "workflow.finished"


def test_handler_registration_rejects_duplicates():
    engine = WorkflowEngine()
    engine.register_handler("noop", lambda ctx: None)
    try:
        engine.register_handler("noop", lambda ctx: None)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "already registered" in str(exc)


if __name__ == "__main__":
    tests = [
        test_successful_refund_workflow,
        test_sensitive_step_blocks_without_approval,
        test_non_refund_skips_refund_and_completes,
        test_retry_succeeds_after_temporary_failure,
        test_failed_step_skips_dependents,
        test_duplicate_step_names_rejected,
        test_unknown_dependency_rejected,
        test_cycle_rejected,
        test_missing_handler_rejected,
        test_missing_condition_rejected,
        test_manifest_contains_execution_order,
        test_run_json_is_serializable,
        test_state_records_step_outputs,
        test_trace_contains_workflow_boundaries,
        test_handler_registration_rejects_duplicates,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
