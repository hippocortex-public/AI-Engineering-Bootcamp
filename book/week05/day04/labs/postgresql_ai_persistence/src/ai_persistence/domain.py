from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4


class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class RunStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def new_id() -> str:
    return str(uuid4())


@dataclass(frozen=True)
class Conversation:
    tenant_id: str
    user_id: str
    title: str
    id: str = field(default_factory=new_id)
    status: str = "active"
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.tenant_id:
            raise ValueError("tenant_id is required")
        if not self.user_id:
            raise ValueError("user_id is required")
        if not self.title:
            raise ValueError("title is required")
        if self.status not in {"active", "archived"}:
            raise ValueError(f"invalid conversation status: {self.status}")


@dataclass(frozen=True)
class Message:
    conversation_id: str
    role: MessageRole
    content: str
    id: str = field(default_factory=new_id)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.conversation_id:
            raise ValueError("conversation_id is required")
        if not isinstance(self.role, MessageRole):
            raise TypeError("role must be a MessageRole")
        if not self.content:
            raise ValueError("content is required")


@dataclass(frozen=True)
class AgentRun:
    conversation_id: str
    model: str
    prompt_version: str
    id: str = field(default_factory=new_id)
    status: RunStatus = RunStatus.RUNNING
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: int | None = None
    error_message: str | None = None
    started_at: datetime = field(default_factory=utc_now)
    finished_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.conversation_id:
            raise ValueError("conversation_id is required")
        if not self.model:
            raise ValueError("model is required")
        if not self.prompt_version:
            raise ValueError("prompt_version is required")
        if not isinstance(self.status, RunStatus):
            raise TypeError("status must be a RunStatus")
        if self.input_tokens < 0 or self.output_tokens < 0:
            raise ValueError("token counts must be positive")
        if self.latency_ms is not None and self.latency_ms < 0:
            raise ValueError("latency_ms must be positive")


@dataclass(frozen=True)
class ToolCall:
    agent_run_id: str
    tool_name: str
    arguments: dict[str, Any]
    id: str = field(default_factory=new_id)
    result: dict[str, Any] | None = None
    status: RunStatus = RunStatus.RUNNING
    latency_ms: int | None = None
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.agent_run_id:
            raise ValueError("agent_run_id is required")
        if not self.tool_name:
            raise ValueError("tool_name is required")
        if not isinstance(self.status, RunStatus):
            raise TypeError("status must be a RunStatus")
