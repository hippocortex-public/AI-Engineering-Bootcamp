from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "examples" / "week01" / "day06"))

from modern_api_patterns import (
    ToolRegistry,
    build_support_request,
    build_tool_enabled_request,
    classify_support_ticket,
    execute_model_tool_call,
    get_order_status,
    parse_tool_call,
    validate_ticket_payload,
)


def test_structured_output_validation_accepts_valid_ticket():
    payload = classify_support_ticket(
        "Urgent production API timeout is blocking checkout for customers."
    )
    assert payload["category"] == "technical"
    assert payload["priority"] == "high"
    assert "blocking checkout" in payload["summary"]


def test_structured_output_validation_rejects_extra_fields():
    with pytest.raises(ValueError, match="Unexpected fields"):
        validate_ticket_payload(
            {
                "category": "technical",
                "priority": "high",
                "summary": "A valid summary string.",
                "confidence": 0.99,
            }
        )


def test_tool_registry_executes_valid_model_tool_call():
    registry = ToolRegistry()
    registry.register("get_order_status", get_order_status)

    result = execute_model_tool_call(
        '{"name":"get_order_status","arguments":{"order_id":"A100"}}',
        registry,
    )

    assert result == {"order_id": "A100", "status": "shipped", "eta_days": 2}


def test_tool_call_parser_rejects_invalid_shape():
    with pytest.raises(ValueError):
        parse_tool_call('{"tool":"get_order_status","args":{"order_id":"A100"}}')


def test_response_request_payload_shapes():
    support = build_support_request("Refund request for an invoice charged twice.")
    payload = support.to_payload()
    assert payload["response_format"]["json_schema"]["strict"] is True
    assert payload["input"][0]["role"] == "user"

    tool_request = build_tool_enabled_request("Where is order A100?")
    tool_payload = tool_request.to_payload()
    assert tool_payload["tools"][0]["name"] == "get_order_status"
