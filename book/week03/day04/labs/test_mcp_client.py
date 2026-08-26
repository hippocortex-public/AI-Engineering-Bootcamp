"""
Tests du lab MCP Client.

Exécution :
    python test_mcp_client.py
"""

from __future__ import annotations

import json
import unittest

from mcp_client import (
    InMemoryMCPServer,
    InMemoryTransport,
    MCPClient,
    MCPClientError,
    MCPServerError,
    MCPSecurityError,
    MCPValidationError,
    ToolResult,
    build_demo_client,
)


class MCPClientTests(unittest.TestCase):
    def make_client(self) -> tuple[MCPClient, InMemoryMCPServer]:
        server = InMemoryMCPServer()
        transport = InMemoryTransport(server)
        client = MCPClient(transport)
        return client, server

    def test_initialize_sets_server_info(self) -> None:
        client, _server = self.make_client()
        result = client.initialize()

        self.assertTrue(client.initialized)
        self.assertEqual(result["serverInfo"]["name"], "bootcamp-mcp-server")
        self.assertEqual(client.server_info["version"], "0.1.0")

    def test_list_tools_requires_initialize(self) -> None:
        client, _server = self.make_client()

        with self.assertRaises(MCPClientError):
            client.list_tools()

    def test_list_tools_returns_tool_specs(self) -> None:
        client = build_demo_client()

        tools = client.list_tools()

        self.assertIn("get_ticket", tools)
        self.assertIn("search_knowledge_base", tools)
        self.assertIn("refund_customer", tools)
        self.assertTrue(tools["refund_customer"].dangerous)

    def test_list_tools_uses_cache(self) -> None:
        client, server = self.make_client()
        client.initialize()

        client.list_tools()
        client.list_tools()

        self.assertEqual(server.list_count, 1)

    def test_refresh_tools_invalidates_cache(self) -> None:
        client, server = self.make_client()
        client.initialize()

        client.list_tools()
        client.refresh_tools()

        self.assertEqual(server.list_count, 2)

    def test_call_tool_success_returns_normalized_result(self) -> None:
        client = build_demo_client()

        result = client.call_tool("get_ticket", {"ticket_id": "INC-42"})

        self.assertIsInstance(result, ToolResult)
        self.assertFalse(result.is_error)
        self.assertEqual(result.structured_content["ticket_id"], "INC-42")
        self.assertEqual(result.structured_content["status"], "open")
        self.assertIn("retrieved", result.message)

    def test_missing_required_argument_is_rejected_locally(self) -> None:
        client = build_demo_client()

        with self.assertRaises(MCPValidationError) as ctx:
            client.call_tool("get_ticket", {})

        self.assertIn("Missing required argument", str(ctx.exception))

    def test_unexpected_argument_is_rejected_locally(self) -> None:
        client = build_demo_client()

        with self.assertRaises(MCPValidationError) as ctx:
            client.call_tool("get_ticket", {"ticket_id": "INC-42", "debug": True})

        self.assertIn("Unexpected argument", str(ctx.exception))

    def test_wrong_type_is_rejected_locally(self) -> None:
        client = build_demo_client()

        with self.assertRaises(MCPValidationError) as ctx:
            client.call_tool("search_knowledge_base", {"query": "mfa", "limit": "3"})

        self.assertIn("limit", str(ctx.exception))

    def test_unknown_local_tool_is_rejected_before_server(self) -> None:
        client = build_demo_client()

        with self.assertRaises(MCPValidationError):
            client.call_tool("delete_everything", {})

    def test_dangerous_tool_requires_approval(self) -> None:
        client = build_demo_client()

        with self.assertRaises(MCPSecurityError):
            client.call_tool(
                "refund_customer",
                {"customer_id": "CUST-42", "amount": 12.5},
            )

        self.assertEqual(client.traces[-1].status, "blocked")

    def test_dangerous_tool_can_run_when_approved(self) -> None:
        client = build_demo_client()

        result = client.call_tool(
            "refund_customer",
            {"customer_id": "CUST-42", "amount": 12.5},
            approved=True,
        )

        self.assertFalse(result.is_error)
        self.assertEqual(result.structured_content["status"], "scheduled")

    def test_agent_registry_wraps_client_tools(self) -> None:
        client = build_demo_client()

        registry = client.as_agent_tools()
        result = registry["get_ticket"]({"ticket_id": "INC-99"})

        self.assertEqual(result.structured_content["ticket_id"], "INC-99")

    def test_server_error_is_mapped(self) -> None:
        client, _server = self.make_client()
        client.initialize()

        with self.assertRaises(MCPServerError):
            client._request("unknown/method", {})

    def test_trace_json_is_serializable(self) -> None:
        client = build_demo_client()
        client.call_tool("get_ticket", {"ticket_id": "INC-42"})

        parsed = json.loads(client.trace_json())

        self.assertEqual(parsed[-1]["tool"], "get_ticket")
        self.assertEqual(parsed[-1]["status"], "success")


if __name__ == "__main__":
    unittest.main(verbosity=2)
