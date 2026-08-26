"""
MCP Server pédagogique — Semaine 3 Jour 3.

Ce module implémente une version locale et testable d'un serveur MCP.

Objectif pédagogique :
- comprendre tools/list ;
- comprendre tools/call ;
- comprendre resources/list et resources/read ;
- comprendre prompts/list et prompts/get ;
- valider les arguments côté serveur ;
- retourner des erreurs JSON-RPC contrôlées ;
- tracer les appels.

Aucune dépendance externe n'est requise.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from time import perf_counter
from typing import Any, Callable


JSON = dict[str, Any]


class MCPError(Exception):
    """Erreur contrôlée retournable sous forme JSON-RPC."""

    def __init__(self, code: int, message: str, data: JSON | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.data = data or {}

    def to_json(self) -> JSON:
        payload: JSON = {"code": self.code, "message": self.message}
        if self.data:
            payload["data"] = self.data
        return payload


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    input_schema: JSON
    handler: Callable[[JSON], JSON]
    risk_level: str = "read"


@dataclass(frozen=True)
class ResourceDefinition:
    uri: str
    name: str
    mime_type: str
    text: str


@dataclass(frozen=True)
class PromptDefinition:
    name: str
    description: str
    template: str
    argument_schema: JSON


@dataclass
class TraceEntry:
    request_id: str | None
    method: str
    status: str
    tool_name: str | None = None
    error_code: int | None = None
    duration_ms: float = 0.0
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_json(self) -> JSON:
        return {
            "request_id": self.request_id,
            "method": self.method,
            "status": self.status,
            "tool_name": self.tool_name,
            "error_code": self.error_code,
            "duration_ms": round(self.duration_ms, 3),
            "timestamp": self.timestamp,
        }


class MCPServer:
    """Serveur MCP minimal en mémoire."""

    JSONRPC_VERSION = "2.0"

    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603
    BUSINESS_ERROR = -32000

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.tools: dict[str, ToolDefinition] = {}
        self.resources: dict[str, ResourceDefinition] = {}
        self.prompts: dict[str, PromptDefinition] = {}
        self.traces: list[TraceEntry] = []

    def register_tool(self, tool: ToolDefinition) -> None:
        if tool.name in self.tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        if tool.risk_level not in {"read", "write", "sensitive"}:
            raise ValueError(f"Invalid risk level: {tool.risk_level}")
        self.tools[tool.name] = tool

    def register_resource(self, resource: ResourceDefinition) -> None:
        if resource.uri in self.resources:
            raise ValueError(f"Resource already registered: {resource.uri}")
        self.resources[resource.uri] = resource

    def register_prompt(self, prompt: PromptDefinition) -> None:
        if prompt.name in self.prompts:
            raise ValueError(f"Prompt already registered: {prompt.name}")
        self.prompts[prompt.name] = prompt

    def handle(self, request: JSON) -> JSON:
        """Traite une requête locale au format JSON-RPC-like."""
        start = perf_counter()
        request_id = request.get("id") if isinstance(request, dict) else None
        method = request.get("method") if isinstance(request, dict) else None
        tool_name: str | None = None

        try:
            self._validate_envelope(request)
            method = request["method"]
            params = request.get("params", {}) or {}

            if method == "tools/call":
                tool_name = params.get("name")

            result = self._dispatch(method, params)
            duration_ms = (perf_counter() - start) * 1000
            self._trace(request_id, method, "ok", tool_name, None, duration_ms)
            return {
                "jsonrpc": self.JSONRPC_VERSION,
                "id": request_id,
                "result": result,
            }

        except MCPError as exc:
            duration_ms = (perf_counter() - start) * 1000
            self._trace(request_id, method or "unknown", "error", tool_name, exc.code, duration_ms)
            return {
                "jsonrpc": self.JSONRPC_VERSION,
                "id": request_id,
                "error": exc.to_json(),
            }
        except Exception as exc:  # Defensive boundary for production-like behavior.
            duration_ms = (perf_counter() - start) * 1000
            self._trace(request_id, method or "unknown", "error", tool_name, self.INTERNAL_ERROR, duration_ms)
            error = MCPError(self.INTERNAL_ERROR, "Internal error", {"detail": str(exc)})
            return {
                "jsonrpc": self.JSONRPC_VERSION,
                "id": request_id,
                "error": error.to_json(),
            }

    def _validate_envelope(self, request: JSON) -> None:
        if not isinstance(request, dict):
            raise MCPError(self.INVALID_REQUEST, "Invalid request", {"reason": "request must be an object"})
        if request.get("jsonrpc") != self.JSONRPC_VERSION:
            raise MCPError(self.INVALID_REQUEST, "Invalid request", {"field": "jsonrpc", "expected": self.JSONRPC_VERSION})
        if "method" not in request:
            raise MCPError(self.INVALID_REQUEST, "Invalid request", {"field": "method", "reason": "required"})
        if not isinstance(request["method"], str):
            raise MCPError(self.INVALID_REQUEST, "Invalid request", {"field": "method", "reason": "must be string"})
        if "params" in request and not isinstance(request["params"], dict):
            raise MCPError(self.INVALID_PARAMS, "Invalid params", {"field": "params", "reason": "must be object"})

    def _dispatch(self, method: str, params: JSON) -> JSON:
        if method == "initialize":
            return self._initialize(params)
        if method == "tools/list":
            return self._tools_list()
        if method == "tools/call":
            return self._tools_call(params)
        if method == "resources/list":
            return self._resources_list()
        if method == "resources/read":
            return self._resources_read(params)
        if method == "prompts/list":
            return self._prompts_list()
        if method == "prompts/get":
            return self._prompts_get(params)
        raise MCPError(self.METHOD_NOT_FOUND, "Method not found", {"method": method})

    def _initialize(self, params: JSON) -> JSON:
        client = params.get("client", "unknown-client")
        if not isinstance(client, str):
            raise MCPError(self.INVALID_PARAMS, "Invalid params", {"field": "client", "reason": "must be string"})
        return {
            "serverInfo": {"name": self.name, "version": self.version},
            "capabilities": {
                "tools": {"listChanged": False},
                "resources": {"subscribe": False, "listChanged": False},
                "prompts": {"listChanged": False},
            },
            "client": client,
        }

    def _tools_list(self) -> JSON:
        tools = []
        for name in sorted(self.tools):
            tool = self.tools[name]
            tools.append({
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema,
                "risk_level": tool.risk_level,
            })
        return {"tools": tools}

    def _tools_call(self, params: JSON) -> JSON:
        name = params.get("name")
        arguments = params.get("arguments", {})

        if not isinstance(name, str):
            raise MCPError(self.INVALID_PARAMS, "Invalid params", {"field": "name", "reason": "must be string"})
        if not isinstance(arguments, dict):
            raise MCPError(self.INVALID_PARAMS, "Invalid params", {"field": "arguments", "reason": "must be object"})
        if name not in self.tools:
            raise MCPError(self.METHOD_NOT_FOUND, "Unknown tool", {"tool": name})

        tool = self.tools[name]
        self._validate_arguments(tool.input_schema, arguments)

        if tool.risk_level == "sensitive" and arguments.get("approved_by_human") is not True:
            raise MCPError(
                self.BUSINESS_ERROR,
                "Human approval required",
                {"tool": name, "field": "approved_by_human"},
            )

        payload = tool.handler(arguments)
        return {
            "content": [{"type": "text", "text": payload["text"]}],
            "structuredContent": payload.get("structuredContent", {}),
            "isError": False,
        }

    def _resources_list(self) -> JSON:
        return {
            "resources": [
                {
                    "uri": resource.uri,
                    "name": resource.name,
                    "mimeType": resource.mime_type,
                }
                for resource in sorted(self.resources.values(), key=lambda item: item.uri)
            ]
        }

    def _resources_read(self, params: JSON) -> JSON:
        uri = params.get("uri")
        if not isinstance(uri, str):
            raise MCPError(self.INVALID_PARAMS, "Invalid params", {"field": "uri", "reason": "must be string"})
        if uri not in self.resources:
            raise MCPError(self.METHOD_NOT_FOUND, "Unknown resource", {"uri": uri})
        resource = self.resources[uri]
        return {
            "contents": [
                {
                    "uri": resource.uri,
                    "mimeType": resource.mime_type,
                    "text": resource.text,
                }
            ]
        }

    def _prompts_list(self) -> JSON:
        return {
            "prompts": [
                {
                    "name": prompt.name,
                    "description": prompt.description,
                    "arguments": prompt.argument_schema,
                }
                for prompt in sorted(self.prompts.values(), key=lambda item: item.name)
            ]
        }

    def _prompts_get(self, params: JSON) -> JSON:
        name = params.get("name")
        arguments = params.get("arguments", {})
        if not isinstance(name, str):
            raise MCPError(self.INVALID_PARAMS, "Invalid params", {"field": "name", "reason": "must be string"})
        if not isinstance(arguments, dict):
            raise MCPError(self.INVALID_PARAMS, "Invalid params", {"field": "arguments", "reason": "must be object"})
        if name not in self.prompts:
            raise MCPError(self.METHOD_NOT_FOUND, "Unknown prompt", {"prompt": name})

        prompt = self.prompts[name]
        self._validate_arguments(prompt.argument_schema, arguments)
        rendered = prompt.template.format(**arguments)
        return {
            "description": prompt.description,
            "messages": [
                {
                    "role": "user",
                    "content": {"type": "text", "text": rendered},
                }
            ],
        }

    def _validate_arguments(self, schema: JSON, arguments: JSON) -> None:
        if schema.get("type") != "object":
            raise MCPError(self.INTERNAL_ERROR, "Invalid tool schema", {"reason": "only object schema supported"})

        properties: dict[str, JSON] = schema.get("properties", {})
        required: list[str] = schema.get("required", [])
        additional = schema.get("additionalProperties", True)

        for field_name in required:
            if field_name not in arguments:
                raise MCPError(self.INVALID_PARAMS, "Invalid params", {"field": field_name, "reason": "required"})

        if additional is False:
            unexpected = sorted(set(arguments) - set(properties))
            if unexpected:
                raise MCPError(
                    self.INVALID_PARAMS,
                    "Invalid params",
                    {"field": unexpected[0], "reason": "unexpected property"},
                )

        for field_name, value in arguments.items():
            if field_name not in properties:
                continue
            field_schema = properties[field_name]
            expected_type = field_schema.get("type")
            if expected_type and not self._matches_type(value, expected_type):
                raise MCPError(
                    self.INVALID_PARAMS,
                    "Invalid params",
                    {"field": field_name, "reason": f"must be {expected_type}"},
                )

            enum = field_schema.get("enum")
            if enum is not None and value not in enum:
                raise MCPError(
                    self.INVALID_PARAMS,
                    "Invalid params",
                    {"field": field_name, "reason": "invalid enum", "allowed": enum},
                )

            min_length = field_schema.get("minLength")
            if min_length is not None and isinstance(value, str) and len(value) < min_length:
                raise MCPError(
                    self.INVALID_PARAMS,
                    "Invalid params",
                    {"field": field_name, "reason": f"minLength {min_length}"},
                )

            minimum = field_schema.get("minimum")
            if minimum is not None and isinstance(value, (int, float)) and value < minimum:
                raise MCPError(
                    self.INVALID_PARAMS,
                    "Invalid params",
                    {"field": field_name, "reason": f"minimum {minimum}"},
                )

    @staticmethod
    def _matches_type(value: Any, expected_type: str) -> bool:
        if expected_type == "string":
            return isinstance(value, str)
        if expected_type == "number":
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        if expected_type == "integer":
            return isinstance(value, int) and not isinstance(value, bool)
        if expected_type == "boolean":
            return isinstance(value, bool)
        if expected_type == "object":
            return isinstance(value, dict)
        if expected_type == "array":
            return isinstance(value, list)
        return True

    def _trace(
        self,
        request_id: str | None,
        method: str,
        status: str,
        tool_name: str | None,
        error_code: int | None,
        duration_ms: float,
    ) -> None:
        self.traces.append(
            TraceEntry(
                request_id=request_id,
                method=method,
                status=status,
                tool_name=tool_name,
                error_code=error_code,
                duration_ms=duration_ms,
            )
        )

    def trace_log(self) -> list[JSON]:
        return [trace.to_json() for trace in self.traces]


def lookup_order_handler(arguments: JSON) -> JSON:
    orders = {
        "ORD-1001": {"order_id": "ORD-1001", "status": "shipped", "total": 79.90},
        "ORD-1002": {"order_id": "ORD-1002", "status": "processing", "total": 129.00},
    }
    order_id = arguments["order_id"]
    order = orders.get(order_id)
    if order is None:
        raise MCPError(MCPServer.BUSINESS_ERROR, "Order not found", {"order_id": order_id})
    return {
        "text": f"Commande {order_id}: {order['status']}",
        "structuredContent": order,
    }


def search_knowledge_base_handler(arguments: JSON) -> JSON:
    query = arguments["query"].lower()
    documents = {
        "refund": "Refunds are allowed within 30 days for eligible orders.",
        "delivery": "Delivery delays above 7 days may trigger a support escalation.",
    }
    matches = [
        {"topic": topic, "text": text}
        for topic, text in documents.items()
        if query in topic or query in text.lower()
    ]
    return {
        "text": f"{len(matches)} document(s) found",
        "structuredContent": {"matches": matches},
    }


def create_support_draft_handler(arguments: JSON) -> JSON:
    message = arguments["customer_message"]
    tone = arguments["tone"]
    language = arguments["language"]
    if language == "fr":
        draft = f"Bonjour, merci pour votre message. Nous allons traiter votre demande avec un ton {tone}: {message}"
    else:
        draft = f"Hello, thank you for your message. We will handle your request in a {tone} tone: {message}"
    return {
        "text": draft,
        "structuredContent": {
            "draft": draft,
            "tone": tone,
            "language": language,
        },
    }


def refund_order_handler(arguments: JSON) -> JSON:
    order_id = arguments["order_id"]
    amount = arguments["amount"]
    reason = arguments["reason"]
    return {
        "text": f"Refund approved for {order_id}: {amount:.2f}",
        "structuredContent": {
            "order_id": order_id,
            "amount": amount,
            "reason": reason,
            "status": "refund_created",
        },
    }


def build_demo_server() -> MCPServer:
    server = MCPServer(name="bootcamp-support-mcp-server", version="0.1.0")

    server.register_tool(
        ToolDefinition(
            name="lookup_order",
            description="Look up a customer order by order_id.",
            risk_level="read",
            input_schema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "minLength": 1}
                },
                "required": ["order_id"],
                "additionalProperties": False,
            },
            handler=lookup_order_handler,
        )
    )

    server.register_tool(
        ToolDefinition(
            name="search_knowledge_base",
            description="Search the support knowledge base.",
            risk_level="read",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "minLength": 1}
                },
                "required": ["query"],
                "additionalProperties": False,
            },
            handler=search_knowledge_base_handler,
        )
    )

    server.register_tool(
        ToolDefinition(
            name="create_support_draft",
            description="Create a support answer draft from a customer message.",
            risk_level="write",
            input_schema={
                "type": "object",
                "properties": {
                    "customer_message": {"type": "string", "minLength": 1},
                    "tone": {"type": "string", "enum": ["professional", "friendly", "concise"]},
                    "language": {"type": "string", "enum": ["fr", "en"]},
                },
                "required": ["customer_message", "tone", "language"],
                "additionalProperties": False,
            },
            handler=create_support_draft_handler,
        )
    )

    server.register_tool(
        ToolDefinition(
            name="refund_order",
            description="Create a refund after explicit human approval.",
            risk_level="sensitive",
            input_schema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "minLength": 1},
                    "amount": {"type": "number", "minimum": 0.01},
                    "reason": {"type": "string", "minLength": 1},
                    "approved_by_human": {"type": "boolean"},
                },
                "required": ["order_id", "amount", "reason", "approved_by_human"],
                "additionalProperties": False,
            },
            handler=refund_order_handler,
        )
    )

    server.register_resource(
        ResourceDefinition(
            uri="kb://support/refunds",
            name="Refund policy",
            mime_type="text/markdown",
            text="Refunds are possible within 30 days for eligible orders. Human approval is required for monetary actions.",
        )
    )
    server.register_resource(
        ResourceDefinition(
            uri="kb://support/escalation",
            name="Escalation policy",
            mime_type="text/markdown",
            text="Escalate legal threats, safety issues, repeated SLA breaches, payment anomalies, and angry VIP customer cases.",
        )
    )

    server.register_prompt(
        PromptDefinition(
            name="support_triage",
            description="Triage a customer support message.",
            argument_schema={
                "type": "object",
                "properties": {
                    "language": {"type": "string", "enum": ["fr", "en"]},
                },
                "required": ["language"],
                "additionalProperties": False,
            },
            template=(
                "Analyse le message client en langue {language}. "
                "Retourne l'intention, le niveau de risque, les informations manquantes "
                "et l'action recommandée."
            ),
        )
    )

    return server


def demo() -> None:
    server = build_demo_server()
    requests = [
        {"jsonrpc": "2.0", "id": "init", "method": "initialize", "params": {"client": "demo"}},
        {"jsonrpc": "2.0", "id": "list", "method": "tools/list"},
        {
            "jsonrpc": "2.0",
            "id": "lookup",
            "method": "tools/call",
            "params": {"name": "lookup_order", "arguments": {"order_id": "ORD-1001"}},
        },
        {
            "jsonrpc": "2.0",
            "id": "refund-denied",
            "method": "tools/call",
            "params": {
                "name": "refund_order",
                "arguments": {
                    "order_id": "ORD-1001",
                    "amount": 20.0,
                    "reason": "late delivery",
                    "approved_by_human": False,
                },
            },
        },
    ]
    for request in requests:
        response = server.handle(request)
        print(response)
    print("TRACE LOG")
    for trace in server.trace_log():
        print(trace)


if __name__ == "__main__":
    demo()
