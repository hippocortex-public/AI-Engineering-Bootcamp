from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mini_framework.observability import Observability, ObservabilityConfig, summarize_export
from book.week04.day06.labs.observability_lab import run_support_agent_demo


def test_trace_completes():
    obs = Observability()
    with obs.start_trace("agent_run") as trace:
        pass
    assert obs.traces[trace.trace_id].status == "completed"


def test_nested_spans_have_parent_child_relation():
    obs = Observability()
    with obs.start_trace("agent_run"):
        with obs.start_span("agent.plan", kind="agent") as parent:
            with obs.start_span("tool.search", kind="tool") as child:
                assert child.parent_id == parent.span_id


def test_event_attaches_to_current_span():
    obs = Observability()
    with obs.start_trace("agent_run"):
        with obs.start_span("tool.search", kind="tool") as span:
            event = obs.record_event("tool_called", "Tool called")
            assert event.span_id == span.span_id
            assert span.events[0].name == "tool_called"


def test_metric_attaches_to_current_context():
    obs = Observability()
    with obs.start_trace("agent_run") as trace:
        with obs.start_span("tool.search", kind="tool") as span:
            metric = obs.record_metric("tool.call.count", 1)
            assert metric.trace_id == trace.trace_id
            assert metric.span_id == span.span_id


def test_sensitive_attributes_are_redacted_by_default():
    obs = Observability()
    with obs.start_trace("agent_run", {"email": "client@example.com"}):
        with obs.start_span("tool.search", attributes={"api_key": "sk-secret", "ticket_id": "TCK-1"}) as span:
            assert span.attributes["api_key"] == "[REDACTED]"
            assert span.attributes["ticket_id"] == "TCK-1"
    payload = obs.export_json()
    assert payload["traces"][0]["attributes"]["email"] == "[REDACTED]"


def test_sensitive_attributes_can_be_included_explicitly():
    obs = Observability(ObservabilityConfig(include_sensitive_data=True))
    with obs.start_trace("agent_run", {"email": "client@example.com"}) as trace:
        pass
    assert obs.traces[trace.trace_id].attributes["email"] == "client@example.com"


def test_exception_marks_span_and_trace_failed():
    obs = Observability()
    try:
        with obs.start_trace("agent_run") as trace:
            with obs.start_span("tool.fail", kind="tool"):
                raise ValueError("boom")
    except ValueError:
        pass

    trace_record = obs.traces[trace.trace_id]
    failed = obs.find_spans(status="failed")
    assert trace_record.status == "failed"
    assert len(failed) == 1
    assert "ValueError" in failed[0].error


def test_capture_exception_can_fail_span_without_crashing_trace():
    obs = Observability()
    with obs.start_trace("agent_run") as trace:
        with obs.start_span("tool.fail", kind="tool"):
            try:
                raise RuntimeError("remote timeout")
            except RuntimeError as exc:
                obs.capture_exception(exc, {"secret": "hidden"})
        with obs.start_span("agent.fallback", kind="agent"):
            obs.record_event("fallback_used", "Safe fallback")
    health = obs.health_report(trace.trace_id)
    assert obs.traces[trace.trace_id].status == "completed"
    assert health["failed_span_count"] == 1
    assert obs.events[0].attributes["secret"] == "[REDACTED]"


def test_export_json_is_serializable():
    payload = run_support_agent_demo()
    encoded = json.dumps(payload)
    assert "support_agent_run" in encoded


def test_latency_summary_contains_span_counts():
    payload = run_support_agent_demo()
    summary = payload["latency_summary"]
    assert summary["span_count"] == 4
    assert "agent" in summary["by_kind"]
    assert "tool" in summary["by_kind"]


def test_trace_tree_reconstructs_roots():
    payload = run_support_agent_demo()
    tree = payload["tree"]
    names = [node["name"] for node in tree]
    assert "agent.classify_request" in names
    assert "tool.search_ticket" in names


def test_health_report_counts_failed_spans():
    obs = Observability()
    with obs.start_trace("agent_run") as trace:
        with obs.start_span("tool.fail", kind="tool"):
            try:
                raise RuntimeError("service unavailable")
            except RuntimeError as exc:
                obs.capture_exception(exc)
    health = obs.health_report(trace.trace_id)
    assert health["failed_span_count"] == 1
    assert health["error_event_count"] == 1


def test_find_spans_filters_by_kind():
    payload = run_support_agent_demo()
    obs = Observability()
    # Build a new collector for a direct filter check.
    with obs.start_trace("agent_run"):
        with obs.start_span("agent.plan", kind="agent"):
            pass
        with obs.start_span("tool.search", kind="tool"):
            pass
    tool_spans = obs.find_spans(kind="tool")
    assert len(tool_spans) == 1
    assert tool_spans[0].name == "tool.search"


def test_summarize_export_counts_errors_and_durations():
    obs = Observability()
    with obs.start_trace("agent_run"):
        with obs.start_span("tool.fail", kind="tool"):
            try:
                raise RuntimeError("x")
            except RuntimeError as exc:
                obs.capture_exception(exc)
    summary = summarize_export(obs.export_json())
    assert summary["trace_count"] == 1
    assert summary["failed_span_count"] == 1
    assert summary["error_event_count"] == 1


def test_lab_demo_redacts_sensitive_values_and_records_guardrail():
    payload = run_support_agent_demo()
    as_text = json.dumps(payload)
    assert "client@example.com" not in as_text
    assert "sk-secret" not in as_text
    event_names = [event["name"] for event in payload["events"]]
    assert "guardrail_blocked" in event_names
    assert payload["health"]["trace_status"] == "completed"


if __name__ == "__main__":
    tests = [
        value
        for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
