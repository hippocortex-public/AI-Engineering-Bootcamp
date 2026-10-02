from __future__ import annotations

from dataclasses import replace
from typing import Protocol

from .domain import AgentRun, Conversation, Message, MessageRole, RunStatus, ToolCall


class ConversationStore(Protocol):
    """Persistence boundary used by the application layer."""

    def create_conversation(self, tenant_id: str, user_id: str, title: str) -> Conversation:
        ...

    def append_message(
        self,
        conversation_id: str,
        role: MessageRole,
        content: str,
        metadata: dict | None = None,
    ) -> Message:
        ...

    def list_messages(self, conversation_id: str) -> list[Message]:
        ...

    def create_agent_run(
        self,
        conversation_id: str,
        model: str,
        prompt_version: str,
    ) -> AgentRun:
        ...

    def complete_agent_run(
        self,
        run_id: str,
        status: RunStatus,
        input_tokens: int = 0,
        output_tokens: int = 0,
        latency_ms: int | None = None,
        error_message: str | None = None,
    ) -> AgentRun:
        ...

    def add_tool_call(
        self,
        agent_run_id: str,
        tool_name: str,
        arguments: dict,
        result: dict | None = None,
        status: RunStatus = RunStatus.SUCCEEDED,
    ) -> ToolCall:
        ...


class InMemoryConversationStore:
    """Deterministic adapter for tests and local exercises.

    This class intentionally mimics the behavior expected from PostgreSQL:
    messages require an existing conversation, runs require an existing
    conversation, and tool calls require an existing run.
    """

    def __init__(self) -> None:
        self._conversations: dict[str, Conversation] = {}
        self._messages: list[Message] = []
        self._runs: dict[str, AgentRun] = {}
        self._tool_calls: list[ToolCall] = []

    def create_conversation(self, tenant_id: str, user_id: str, title: str) -> Conversation:
        conversation = Conversation(tenant_id=tenant_id, user_id=user_id, title=title)
        self._conversations[conversation.id] = conversation
        return conversation

    def append_message(
        self,
        conversation_id: str,
        role: MessageRole,
        content: str,
        metadata: dict | None = None,
    ) -> Message:
        self._require_conversation(conversation_id)
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            metadata=metadata or {},
        )
        self._messages.append(message)
        return message

    def list_messages(self, conversation_id: str) -> list[Message]:
        self._require_conversation(conversation_id)
        return [m for m in self._messages if m.conversation_id == conversation_id]

    def create_agent_run(
        self,
        conversation_id: str,
        model: str,
        prompt_version: str,
    ) -> AgentRun:
        self._require_conversation(conversation_id)
        run = AgentRun(
            conversation_id=conversation_id,
            model=model,
            prompt_version=prompt_version,
        )
        self._runs[run.id] = run
        return run

    def complete_agent_run(
        self,
        run_id: str,
        status: RunStatus,
        input_tokens: int = 0,
        output_tokens: int = 0,
        latency_ms: int | None = None,
        error_message: str | None = None,
    ) -> AgentRun:
        if run_id not in self._runs:
            raise KeyError(f"unknown agent run: {run_id}")
        if status not in {RunStatus.SUCCEEDED, RunStatus.FAILED}:
            raise ValueError("final status must be succeeded or failed")

        current = self._runs[run_id]
        completed = replace(
            current,
            status=status,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            error_message=error_message,
        )
        self._runs[run_id] = completed
        return completed

    def add_tool_call(
        self,
        agent_run_id: str,
        tool_name: str,
        arguments: dict,
        result: dict | None = None,
        status: RunStatus = RunStatus.SUCCEEDED,
    ) -> ToolCall:
        if agent_run_id not in self._runs:
            raise KeyError(f"unknown agent run: {agent_run_id}")
        tool_call = ToolCall(
            agent_run_id=agent_run_id,
            tool_name=tool_name,
            arguments=arguments,
            result=result,
            status=status,
        )
        self._tool_calls.append(tool_call)
        return tool_call

    def _require_conversation(self, conversation_id: str) -> None:
        if conversation_id not in self._conversations:
            raise KeyError(f"unknown conversation: {conversation_id}")


class PostgresConversationStore:
    """Minimal PostgreSQL adapter skeleton.

    It is not used by the tests because the bootcamp lab must be executable
    without external infrastructure. In production, pass a psycopg connection
    or connection pool and execute the SQL inside transactions.
    """

    def __init__(self, connection) -> None:
        self.connection = connection

    def create_conversation(self, tenant_id: str, user_id: str, title: str) -> Conversation:
        query = """
        insert into conversations (tenant_id, user_id, title)
        values (%s, %s, %s)
        returning id, tenant_id, user_id, title, status, metadata, created_at, updated_at
        """
        with self.connection.cursor() as cur:
            cur.execute(query, (tenant_id, user_id, title))
            row = cur.fetchone()
        self.connection.commit()
        return Conversation(
            id=str(row[0]),
            tenant_id=row[1],
            user_id=row[2],
            title=row[3],
            status=row[4],
            metadata=row[5],
            created_at=row[6],
            updated_at=row[7],
        )
