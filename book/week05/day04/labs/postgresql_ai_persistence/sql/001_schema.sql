-- 001_schema.sql
-- PostgreSQL schema for an AI assistant persistence layer.

create extension if not exists pgcrypto;

create table if not exists conversations (
    id uuid primary key default gen_random_uuid(),
    tenant_id text not null,
    user_id text not null,
    title text not null,
    status text not null default 'active'
        check (status in ('active', 'archived')),
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists messages (
    id uuid primary key default gen_random_uuid(),
    conversation_id uuid not null
        references conversations(id)
        on delete cascade,
    role text not null
        check (role in ('system', 'user', 'assistant', 'tool')),
    content text not null,
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create table if not exists agent_runs (
    id uuid primary key default gen_random_uuid(),
    conversation_id uuid not null
        references conversations(id)
        on delete cascade,
    status text not null default 'running'
        check (status in ('pending', 'running', 'succeeded', 'failed')),
    model text not null,
    prompt_version text not null,
    input_tokens integer not null default 0
        check (input_tokens >= 0),
    output_tokens integer not null default 0
        check (output_tokens >= 0),
    latency_ms integer
        check (latency_ms is null or latency_ms >= 0),
    error_message text,
    started_at timestamptz not null default now(),
    finished_at timestamptz
);

create table if not exists tool_calls (
    id uuid primary key default gen_random_uuid(),
    agent_run_id uuid not null
        references agent_runs(id)
        on delete cascade,
    tool_name text not null,
    arguments jsonb not null default '{}'::jsonb,
    result jsonb,
    status text not null default 'running'
        check (status in ('pending', 'running', 'succeeded', 'failed')),
    latency_ms integer
        check (latency_ms is null or latency_ms >= 0),
    created_at timestamptz not null default now()
);

create table if not exists evaluations (
    id uuid primary key default gen_random_uuid(),
    agent_run_id uuid not null
        references agent_runs(id)
        on delete cascade,
    metric_name text not null,
    score numeric not null
        check (score >= 0 and score <= 1),
    comment text,
    created_at timestamptz not null default now()
);
