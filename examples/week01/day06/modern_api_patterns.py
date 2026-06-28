"""
Week 01 Day 06 — Modern LLM API Patterns.

This module intentionally avoids external network calls.
It models three production-grade concepts used with modern LLM APIs:

1. A Responses-style request envelope.
2. Structured Outputs validation.
3. Tool Calling orchestration.

The objective is to make the mechanics testable before connecting a real provider SDK.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Literal, Optional
import json


MessageRole = Literal["system", "user", "assistant", "tool"]


@dataclass(frozen=True)
class Message:
    role: MessageRole
    content: str


@dataclass(frozen=True)
class ResponseRequest:
    model: str
    instructions: str
    input: List[Message]
    response_format: Optional[Dict[str, Any]] = None
    tools: Optional[List[Dict[str, Any]]] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "instructions": self.instructions,
            "input": [{"role": m.role, "content": m.content} for m in self.input],
        }
        if self.response_format is not None:
            payload["response_format"] = self.response_format
        if self.tools is not None:
            payload["tools"] = self.tools
        return payload


TICKET_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["category", "priority", "summary"],
    "properties": {
        "category": {"type": "string", "enum": ["billing", "technical", "account", "other"]},
        "priority": {"type": "string", "enum": ["low", "medium", "high"]},
        "summary": {"type": "string", "minLength": 12},
    },
    "additionalProperties": False,
}


def validate_ticket_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a minimal structured output without third-party dependencies."""
    required = TICKET_SCHEMA["required"]
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    allowed = set(TICKET_SCHEMA["properties"].keys())
    extra = sorted(set(payload.keys()) - allowed)
    if extra:
        raise ValueError(f"Unexpected fields: {extra}")

    category = payload["category"]
    priority = payload["priority"]
    summary = payload["summary"]

    if category not in TICKET_SCHEMA["properties"]["category"]["enum"]:
        raise ValueError(f"Invalid category: {category}")
    if priority not in TICKET_SCHEMA["properties"]["priority"]["enum"]:
        raise ValueError(f"Invalid priority: {priority}")
    if not isinstance(summary, str) or len(summary) < 12:
        raise ValueError("Summary must be a string with at least 12 characters")

    return payload


def classify_support_ticket(text: str) -> Dict[str, str]:
    """A deterministic mock that simulates a structured model response."""
    lowered = text.lower()

    if any(word in lowered for word in ["invoice", "billing", "payment", "refund", "charge"]):
        category = "billing"
    elif any(word in lowered for word in ["bug", "error", "api", "timeout", "crash", "token"]):
        category = "technical"
    elif any(word in lowered for word in ["login", "password", "account", "email"]):
        category = "account"
    else:
        category = "other"

    if any(word in lowered for word in ["urgent", "production", "blocked", "down", "critical"]):
        priority = "high"
    elif any(word in lowered for word in ["soon", "issue", "problem", "slow"]):
        priority = "medium"
    else:
        priority = "low"

    summary = text.strip()
    if len(summary) > 80:
        summary = summary[:77].rstrip() + "..."
    if len(summary) < 12:
        summary = f"Customer request: {summary}"

    return validate_ticket_payload(
        {"category": category, "priority": priority, "summary": summary}
    )


ToolFunction = Callable[..., Dict[str, Any]]


class ToolRegistry:
    """Small tool registry used to demonstrate safe function dispatch."""

    def __init__(self) -> None:
        self._tools: Dict[str, ToolFunction] = {}

    def register(self, name: str, function: ToolFunction) -> None:
        if not name or not name.replace("_", "").isalnum():
            raise ValueError("Tool name must be alphanumeric or underscore")
        self._tools[name] = function

    def call(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        if not isinstance(arguments, dict):
            raise TypeError("Tool arguments must be a dictionary")
        return self._tools[name](**arguments)


def get_order_status(order_id: str) -> Dict[str, Any]:
    """Deterministic fake business tool."""
    data = {
        "A100": {"status": "shipped", "eta_days": 2},
        "B200": {"status": "processing", "eta_days": 5},
        "C300": {"status": "delayed", "eta_days": 9},
    }
    return {"order_id": order_id, **data.get(order_id, {"status": "unknown", "eta_days": None})}


def parse_tool_call(raw: str) -> Dict[str, Any]:
    """
    Parse a model-emitted tool call.

    Expected shape:
    {
      "name": "get_order_status",
      "arguments": {"order_id": "A100"}
    }
    """
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("Tool call must be valid JSON") from exc

    if set(payload.keys()) != {"name", "arguments"}:
        raise ValueError("Tool call must contain exactly name and arguments")
    if not isinstance(payload["name"], str):
        raise ValueError("Tool name must be a string")
    if not isinstance(payload["arguments"], dict):
        raise ValueError("Tool arguments must be an object")
    return payload


def execute_model_tool_call(raw: str, registry: ToolRegistry) -> Dict[str, Any]:
    call = parse_tool_call(raw)
    return registry.call(call["name"], call["arguments"])


def build_support_request(ticket_text: str) -> ResponseRequest:
    return ResponseRequest(
        model="example-modern-llm",
        instructions=(
            "Classify the support ticket. Return only data matching the provided schema."
        ),
        input=[Message(role="user", content=ticket_text)],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "support_ticket_classification",
                "schema": TICKET_SCHEMA,
                "strict": True,
            },
        },
    )


def build_tool_enabled_request(question: str) -> ResponseRequest:
    return ResponseRequest(
        model="example-modern-llm",
        instructions=(
            "Answer the user. When the order status is required, call the order status tool."
        ),
        input=[Message(role="user", content=question)],
        tools=[
            {
                "type": "function",
                "name": "get_order_status",
                "description": "Return status and ETA for a customer order.",
                "parameters": {
                    "type": "object",
                    "required": ["order_id"],
                    "properties": {"order_id": {"type": "string"}},
                    "additionalProperties": False,
                },
            }
        ],
    )
