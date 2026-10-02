from __future__ import annotations


def list_messages_query() -> tuple[str, tuple[str, ...]]:
    """Return a parameterized query for reconstructing a conversation."""
    sql = """
    select id, conversation_id, role, content, metadata, created_at
    from messages
    where conversation_id = %s
    order by created_at asc
    """
    return sql.strip(), ("conversation_id",)


def failed_runs_query(limit: int = 50) -> tuple[str, tuple[int]]:
    """Return a safe query for recent failed runs.

    The limit is passed as a bind parameter to preserve a consistent
    parameterization style.
    """
    if limit <= 0 or limit > 500:
        raise ValueError("limit must be between 1 and 500")

    sql = """
    select id, conversation_id, model, prompt_version, error_message, started_at
    from agent_runs
    where status = 'failed'
    order by started_at desc
    limit %s
    """
    return sql.strip(), (limit,)


def average_latency_by_model_query() -> str:
    return """
    select model, avg(latency_ms) as avg_latency_ms
    from agent_runs
    where status = 'succeeded'
    group by model
    order by avg_latency_ms desc
    """.strip()


def insert_message_query() -> tuple[str, tuple[str, str, str]]:
    sql = """
    insert into messages (conversation_id, role, content)
    values (%s, %s, %s)
    returning id, conversation_id, role, content, metadata, created_at
    """
    return sql.strip(), ("conversation_id", "role", "content")
