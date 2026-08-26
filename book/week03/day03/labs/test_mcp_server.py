"""
Tests du MCP Server pédagogique.
Exécution :
    python test_mcp_server.py
"""

from mcp_server import MCPServer, build_demo_server


def assert_ok(response):
    assert "result" in response, response
    assert "error" not in response, response


def assert_error(response, code):
    assert "error" in response, response
    assert response["error"]["code"] == code, response


def test_initialize_returns_capabilities():
    server = build_demo_server()
    response = server.handle({
        "jsonrpc": "2.0",
        "id": "init-1",
        "method": "initialize",
        "params": {"client": "test-client"},
    })
    assert_ok(response)
    result = response["result"]
    assert result["serverInfo"]["name"] == "bootcamp-support-mcp-server"
    assert "tools" in result["capabilities"]
    assert "resources" in result["capabilities"]
    assert "prompts" in result["capabilities"]


def test_tools_list_is_deterministic_and_exposes_risk_level():
    server = build_demo_server()
    response = server.handle({"jsonrpc": "2.0", "id": "tools-1", "method": "tools/list"})
    assert_ok(response)
    names = [tool["name"] for tool in response["result"]["tools"]]
    assert names == sorted(names)
    assert "lookup_order" in names
    refund = next(tool for tool in response["result"]["tools"] if tool["name"] == "refund_order")
    assert refund["risk_level"] == "sensitive"


def test_lookup_order_success():
    server = build_demo_server()
    response = server.handle({
        "jsonrpc": "2.0",
        "id": "call-1",
        "method": "tools/call",
        "params": {"name": "lookup_order", "arguments": {"order_id": "ORD-1001"}},
    })
    assert_ok(response)
    assert response["result"]["structuredContent"]["status"] == "shipped"
    assert response["result"]["isError"] is False


def test_lookup_order_missing_required_argument_is_rejected():
    server = build_demo_server()
    response = server.handle({
        "jsonrpc": "2.0",
        "id": "call-2",
        "method": "tools/call",
        "params": {"name": "lookup_order", "arguments": {}},
    })
    assert_error(response, MCPServer.INVALID_PARAMS)
    assert response["error"]["data"]["field"] == "order_id"


def test_unexpected_property_is_rejected():
    server = build_demo_server()
    response = server.handle({
        "jsonrpc": "2.0",
        "id": "call-3",
        "method": "tools/call",
        "params": {
            "name": "lookup_order",
            "arguments": {"order_id": "ORD-1001", "debug": True},
        },
    })
    assert_error(response, MCPServer.INVALID_PARAMS)
    assert response["error"]["data"]["reason"] == "unexpected property"


def test_unknown_tool_is_rejected():
    server = build_demo_server()
    response = server.handle({
        "jsonrpc": "2.0",
        "id": "call-4",
        "method": "tools/call",
        "params": {"name": "delete_everything", "arguments": {}},
    })
    assert_error(response, MCPServer.METHOD_NOT_FOUND)


def test_resource_read_success():
    server = build_demo_server()
    response = server.handle({
        "jsonrpc": "2.0",
        "id": "res-1",
        "method": "resources/read",
        "params": {"uri": "kb://support/refunds"},
    })
    assert_ok(response)
    contents = response["result"]["contents"]
    assert contents[0]["uri"] == "kb://support/refunds"
    assert "Refunds" in contents[0]["text"]


def test_prompts_get_success():
    server = build_demo_server()
    response = server.handle({
        "jsonrpc": "2.0",
        "id": "prompt-1",
        "method": "prompts/get",
        "params": {"name": "support_triage", "arguments": {"language": "fr"}},
    })
    assert_ok(response)
    messages = response["result"]["messages"]
    assert messages[0]["role"] == "user"
    assert "fr" in messages[0]["content"]["text"]


def test_prompt_argument_validation():
    server = build_demo_server()
    response = server.handle({
        "jsonrpc": "2.0",
        "id": "prompt-2",
        "method": "prompts/get",
        "params": {"name": "support_triage", "arguments": {"language": "de"}},
    })
    assert_error(response, MCPServer.INVALID_PARAMS)
    assert response["error"]["data"]["reason"] == "invalid enum"


def test_sensitive_refund_requires_human_approval():
    server = build_demo_server()
    response = server.handle({
        "jsonrpc": "2.0",
        "id": "refund-1",
        "method": "tools/call",
        "params": {
            "name": "refund_order",
            "arguments": {
                "order_id": "ORD-1001",
                "amount": 10.0,
                "reason": "late delivery",
                "approved_by_human": False,
            },
        },
    })
    assert_error(response, MCPServer.BUSINESS_ERROR)
    assert response["error"]["message"] == "Human approval required"


def test_sensitive_refund_success_with_approval():
    server = build_demo_server()
    response = server.handle({
        "jsonrpc": "2.0",
        "id": "refund-2",
        "method": "tools/call",
        "params": {
            "name": "refund_order",
            "arguments": {
                "order_id": "ORD-1001",
                "amount": 10.0,
                "reason": "late delivery",
                "approved_by_human": True,
            },
        },
    })
    assert_ok(response)
    assert response["result"]["structuredContent"]["status"] == "refund_created"


def test_trace_log_records_success_and_error():
    server = build_demo_server()
    server.handle({"jsonrpc": "2.0", "id": "ok", "method": "tools/list"})
    server.handle({
        "jsonrpc": "2.0",
        "id": "bad",
        "method": "tools/call",
        "params": {"name": "lookup_order", "arguments": {}},
    })
    traces = server.trace_log()
    assert len(traces) == 2
    assert traces[0]["status"] == "ok"
    assert traces[1]["status"] == "error"
    assert traces[1]["tool_name"] == "lookup_order"
    assert traces[1]["error_code"] == MCPServer.INVALID_PARAMS


def run_all_tests():
    tests = [
        test_initialize_returns_capabilities,
        test_tools_list_is_deterministic_and_exposes_risk_level,
        test_lookup_order_success,
        test_lookup_order_missing_required_argument_is_rejected,
        test_unexpected_property_is_rejected,
        test_unknown_tool_is_rejected,
        test_resource_read_success,
        test_prompts_get_success,
        test_prompt_argument_validation,
        test_sensitive_refund_requires_human_approval,
        test_sensitive_refund_success_with_approval,
        test_trace_log_records_success_and_error,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")


if __name__ == "__main__":
    run_all_tests()
