-- 002_indexes.sql
-- Indexes derived from expected production queries.

create index if not exists idx_conversations_tenant_user_created
on conversations (tenant_id, user_id, created_at desc);

create index if not exists idx_messages_conversation_created
on messages (conversation_id, created_at asc);

create index if not exists idx_agent_runs_status_started
on agent_runs (status, started_at desc);

create index if not exists idx_agent_runs_model_started
on agent_runs (model, started_at desc);

create index if not exists idx_tool_calls_run_created
on tool_calls (agent_run_id, created_at asc);

create index if not exists idx_evaluations_metric_created
on evaluations (metric_name, created_at desc);
