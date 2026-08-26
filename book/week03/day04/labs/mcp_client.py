"""
Semaine 3 — Jour 4 — MCP Client

Client MCP pédagogique en Python standard library.

Objectifs :
- initialiser une session ;
- découvrir les tools ;
- valider les arguments localement ;
- appeler tools/call ;
- adapter les tools MCP en registry d'outils agentique ;
- tracer les appels.

Ce module n'implémente pas tout MCP. Il modélise les concepts utiles
pour l'apprentissage AI Engineering sans dépendance externe.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Callable
import json
import time


class MCPClientError(Exception):
    """Erreur générique côté client MCP."""


class MCPValidationError(MCPClientError):
    """Erreur détectée avant l'appel serveur."""


class MCPSecurityError(MCPClientError):
    """Erreur de politique de sécurité côté client."""


class MCPServerError(MCPClientError):
    """Erreur retournée par le serveur MCP."""


@dataclass(frozen=True)
class ToolSpec:
    """Définition locale d'un tool MCP."""

    name: str
    description: str
    input_schema: dict[str, Any]
    dangerous: bool = False


@dataclass
class ToolResult:
    """Observation normalisée retournée à l'agent."""

    tool: str
    is_error: bool
    content: list[dict[str, Any]] = field(default_factory=list)
    structured_content: dict[str, Any] | None = None
    message: str | None = None


@dataclass
class TraceEvent:
    """Événement de trace côté client."""

    request_id: int
    method: str
    status: str
    tool: str | None = None
    duration_ms: int = 0
    error: str | None = None


class InMemoryMCPServer:
    """
    Serveur MCP simulé.

    Le jour 3 a introduit le rôle du serveur.
    Ici, il sert uniquement de cible de test pour le client.
    """

    def __init__(self) -> None:
        self.initialized = False
        self.list_count = 0
        self.tools: dict[str, dict[str, Any]] = {
            "get_ticket": {
                "name": "get_ticket",
                "description": "Retourne le détail d'un ticket support.",
                "inputSchema": {
                    "type": "object",
                    "required": ["ticket_id"],
                    "properties": {
                        "ticket_id": {"type": "string"},
                    },
                    "additionalProperties": False,
                },
                "dangerous": False,
            },
            "search_knowledge_base": {
                "name": "search_knowledge_base",
                "description": "Recherche une solution dans la base de connaissance.",
                "inputSchema": {
                    "type": "object",
                    "required": ["query"],
                    "properties": {
                        "query": {"type": "string"},
                        "limit": {"type": "integer"},
                    },
                    "additionalProperties": False,
                },
                "dangerous": False,
            },
            "refund_customer": {
                "name": "refund_customer",
                "description": "Déclenche un remboursement client.",
                "inputSchema": {
                    "type": "object",
                    "required": ["customer_id", "amount"],
                    "properties": {
                        "customer_id": {"type": "string"},
                        "amount": {"type": "number"},
                        "reason": {"type": "string"},
                    },
                    "additionalProperties": False,
                },
                "dangerous": True,
            },
        }

    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        """Traite une requête JSON-RPC simplifiée."""

        if request.get("jsonrpc") != "2.0":
            return self._error(request.get("id"), -32600, "Invalid JSON-RPC version")

        method = request.get("method")
        request_id = request.get("id")

        if method == "initialize":
            self.initialized = True
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2026-07-28",
                    "serverInfo": {"name": "bootcamp-mcp-server", "version": "0.1.0"},
                    "capabilities": {"tools": {}},
                },
            }

        if not self.initialized:
            return self._error(request_id, -32002, "Server not initialized")

        if method == "tools/list":
            self.list_count += 1
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"tools": list(self.tools.values())},
            }

        if method == "tools/call":
            params = request.get("params") or {}
            tool_name = params.get("name")
            arguments = params.get("arguments") or {}

            if tool_name not in self.tools:
                return self._error(request_id, -32602, f"Unknown tool: {tool_name}")

            if tool_name == "get_ticket":
                ticket_id = arguments["ticket_id"]
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Ticket {ticket_id} retrieved"}],
                        "structuredContent": {
                            "ticket_id": ticket_id,
                            "status": "open",
                            "priority": "high",
                        },
                        "isError": False,
                    },
                }

            if tool_name == "search_knowledge_base":
                query = arguments["query"]
                limit = arguments.get("limit", 3)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"{limit} result(s) for query: {query}",
                            }
                        ],
                        "structuredContent": {
                            "query": query,
                            "matches": [
                                {
                                    "title": "Reset MFA",
                                    "score": 0.91,
                                }
                            ][:limit],
                        },
                        "isError": False,
                    },
                }

            if tool_name == "refund_customer":
                amount = arguments["amount"]
                customer_id = arguments["customer_id"]
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": "Refund scheduled"}],
                        "structuredContent": {
                            "customer_id": customer_id,
                            "amount": amount,
                            "status": "scheduled",
                        },
                        "isError": False,
                    },
                }

        return self._error(request_id, -32601, f"Unknown method: {method}")

    def _error(self, request_id: Any, code: int, message: str) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        }


class InMemoryTransport:
    """Transport synchrone en mémoire pour tester le client sans réseau."""

    def __init__(self, server: InMemoryMCPServer) -> None:
        self.server = server
        self.sent_requests: list[dict[str, Any]] = []

    def send(self, request: dict[str, Any]) -> dict[str, Any]:
        self.sent_requests.append(json.loads(json.dumps(request)))
        return self.server.handle(request)


class MCPClient:
    """Client MCP minimal orienté AI Engineering."""

    def __init__(
        self,
        transport: InMemoryTransport,
        client_name: str = "bootcamp-mcp-client",
        client_version: str = "0.1.0",
    ) -> None:
        self.transport = transport
        self.client_name = client_name
        self.client_version = client_version
        self.initialized = False
        self.server_info: dict[str, Any] | None = None
        self._request_id = 0
        self._tool_cache: dict[str, ToolSpec] | None = None
        self.traces: list[TraceEvent] = []

    def initialize(self) -> dict[str, Any]:
        """Initialise la relation client/serveur."""

        result = self._request(
            "initialize",
            {
                "clientInfo": {
                    "name": self.client_name,
                    "version": self.client_version,
                },
                "clientCapabilities": {"tools": {}},
            },
        )
        self.initialized = True
        self.server_info = result.get("serverInfo")
        return result

    def list_tools(self, use_cache: bool = True) -> dict[str, ToolSpec]:
        """Découvre les tools exposés par le serveur."""

        self._ensure_initialized()

        if use_cache and self._tool_cache is not None:
            return self._tool_cache

        result = self._request("tools/list", {})
        tools: dict[str, ToolSpec] = {}
        for raw_tool in result.get("tools", []):
            spec = ToolSpec(
                name=raw_tool["name"],
                description=raw_tool.get("description", ""),
                input_schema=raw_tool.get("inputSchema", {"type": "object"}),
                dangerous=bool(raw_tool.get("dangerous", False)),
            )
            tools[spec.name] = spec

        self._tool_cache = tools
        return tools

    def refresh_tools(self) -> dict[str, ToolSpec]:
        """Invalide le cache et redécouvre les tools."""

        self._tool_cache = None
        return self.list_tools(use_cache=False)

    def call_tool(
        self,
        name: str,
        arguments: dict[str, Any],
        *,
        approved: bool = False,
    ) -> ToolResult:
        """Valide et appelle un tool MCP."""

        self._ensure_initialized()
        tools = self.list_tools()
        if name not in tools:
            raise MCPValidationError(f"Unknown local tool: {name}")

        spec = tools[name]
        self._validate_arguments(spec, arguments)

        if spec.dangerous and not approved:
            self._record_trace(
                request_id=self._request_id + 1,
                method="tools/call",
                status="blocked",
                tool=name,
                duration_ms=0,
                error="approval_required",
            )
            raise MCPSecurityError(f"Tool '{name}' requires explicit approval")

        start = time.perf_counter()
        try:
            result = self._request(
                "tools/call",
                {"name": name, "arguments": arguments},
                trace_tool=name,
            )
            duration_ms = int((time.perf_counter() - start) * 1000)
            self._record_trace(
                request_id=self._request_id,
                method="tools/call",
                status="success",
                tool=name,
                duration_ms=duration_ms,
            )
            return ToolResult(
                tool=name,
                is_error=bool(result.get("isError", False)),
                content=result.get("content", []),
                structured_content=result.get("structuredContent"),
                message=self._first_text(result.get("content", [])),
            )
        except MCPClientError as exc:
            duration_ms = int((time.perf_counter() - start) * 1000)
            self._record_trace(
                request_id=self._request_id,
                method="tools/call",
                status="error",
                tool=name,
                duration_ms=duration_ms,
                error=str(exc),
            )
            raise

    def as_agent_tools(self) -> dict[str, Callable[[dict[str, Any]], ToolResult]]:
        """Expose les tools MCP comme fonctions appelables par un agent."""

        registry: dict[str, Callable[[dict[str, Any]], ToolResult]] = {}

        for tool_name in self.list_tools():
            def make_wrapper(name: str) -> Callable[[dict[str, Any]], ToolResult]:
                def wrapper(arguments: dict[str, Any]) -> ToolResult:
                    return self.call_tool(name, arguments)
                return wrapper

            registry[tool_name] = make_wrapper(tool_name)

        return registry

    def trace_json(self) -> str:
        """Retourne les traces sous forme JSON."""

        return json.dumps([asdict(event) for event in self.traces], indent=2, ensure_ascii=False)

    def _request(
        self,
        method: str,
        params: dict[str, Any],
        *,
        trace_tool: str | None = None,
    ) -> dict[str, Any]:
        """Envoie une requête JSON-RPC simplifiée."""

        self._request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": method,
            "params": params,
        }

        response = self.transport.send(request)

        if "error" in response:
            error = response["error"]
            message = error.get("message", "Unknown server error")
            raise MCPServerError(f"{error.get('code')}: {message}")

        return response.get("result", {})

    def _ensure_initialized(self) -> None:
        if not self.initialized:
            raise MCPClientError("Client is not initialized")

    def _validate_arguments(self, spec: ToolSpec, arguments: dict[str, Any]) -> None:
        schema = spec.input_schema

        if schema.get("type") != "object":
            raise MCPValidationError(f"Tool '{spec.name}' schema must be an object")

        if not isinstance(arguments, dict):
            raise MCPValidationError("Tool arguments must be an object")

        required = schema.get("required", [])
        properties = schema.get("properties", {})

        for field_name in required:
            if field_name not in arguments:
                raise MCPValidationError(f"Missing required argument: {field_name}")

        if schema.get("additionalProperties") is False:
            extra = set(arguments) - set(properties)
            if extra:
                extra_list = ", ".join(sorted(extra))
                raise MCPValidationError(f"Unexpected argument(s): {extra_list}")

        for field_name, value in arguments.items():
            if field_name not in properties:
                continue
            expected_type = properties[field_name].get("type")
            if not self._matches_type(value, expected_type):
                raise MCPValidationError(
                    f"Argument '{field_name}' must be {expected_type}, got {type(value).__name__}"
                )

    def _matches_type(self, value: Any, expected_type: str | None) -> bool:
        if expected_type is None:
            return True
        if expected_type == "string":
            return isinstance(value, str)
        if expected_type == "integer":
            return isinstance(value, int) and not isinstance(value, bool)
        if expected_type == "number":
            return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
        if expected_type == "boolean":
            return isinstance(value, bool)
        if expected_type == "object":
            return isinstance(value, dict)
        if expected_type == "array":
            return isinstance(value, list)
        return True

    def _record_trace(
        self,
        request_id: int,
        method: str,
        status: str,
        tool: str | None = None,
        duration_ms: int = 0,
        error: str | None = None,
    ) -> None:
        self.traces.append(
            TraceEvent(
                request_id=request_id,
                method=method,
                status=status,
                tool=tool,
                duration_ms=duration_ms,
                error=error,
            )
        )

    def _first_text(self, content: list[dict[str, Any]]) -> str | None:
        for item in content:
            if item.get("type") == "text":
                return item.get("text")
        return None


def build_demo_client() -> MCPClient:
    """Factory utile pour le notebook et les tests."""

    server = InMemoryMCPServer()
    transport = InMemoryTransport(server)
    client = MCPClient(transport)
    client.initialize()
    return client


if __name__ == "__main__":
    client = build_demo_client()
    print("Tools disponibles:")
    for tool in client.list_tools().values():
        marker = " ⚠️" if tool.dangerous else ""
        print(f"- {tool.name}{marker}: {tool.description}")

    result = client.call_tool("get_ticket", {"ticket_id": "INC-42"})
    print("\nRésultat:")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))

    print("\nTrace:")
    print(client.trace_json())
