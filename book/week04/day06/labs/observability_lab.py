from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mini_framework.observability import Observability, ObservabilityConfig, summarize_export


def run_support_agent_demo() -> dict:
    """Run a deterministic support-agent scenario with observability enabled."""

    obs = Observability(
        ObservabilityConfig(
            service_name="bootcamp_support_agent",
            include_sensitive_data=False,
        )
    )

    with obs.start_trace(
        "support_agent_run",
        attributes={"channel": "chat", "user_email": "client@example.com"},
    ) as trace:
        with obs.start_span("agent.classify_request", kind="agent", attributes={"model": "fake-model"}):
            obs.record_event("intent_classified", "Request classified as ticket_status")
            obs.record_metric("agent.step.count", 1, "count", {"step": "classify"})

        with obs.start_span("tool.search_ticket", kind="tool", attributes={"email": "client@example.com", "ticket_id": "TCK-1001"}):
            obs.record_event("tool_arguments_validated", "Tool arguments validated")
            obs.record_metric("tool.call.count", 1, "count", {"tool": "search_ticket"})

        with obs.start_span("guardrail.require_approval", kind="guardrail", attributes={"action": "refund", "api_key": "sk-secret"}):
            obs.record_event(
                "guardrail_blocked",
                "Sensitive action requires human approval",
                level="warning",
                attributes={"user_email": "client@example.com", "action": "refund"},
            )
            obs.record_metric("guardrail.blocked.count", 1, "count", {"action": "refund"})

        with obs.start_span("agent.final_response", kind="agent"):
            obs.record_event("final_response_created", "Safe response produced")

    payload = obs.export_json()
    payload["summary"] = summarize_export(payload)
    payload["trace_id"] = trace.trace_id
    payload["health"] = obs.health_report(trace.trace_id)
    payload["tree"] = obs.trace_tree(trace.trace_id)
    return payload


if __name__ == "__main__":
    import json

    print(json.dumps(run_support_agent_demo(), indent=2, ensure_ascii=False))
