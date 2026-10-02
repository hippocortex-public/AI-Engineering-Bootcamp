-- 003_seed.sql
-- Example data for local exploration.

insert into conversations (tenant_id, user_id, title, metadata)
values (
    'tenant_acme',
    'user_001',
    'Support assistant investigation',
    '{"environment": "local", "source": "seed"}'::jsonb
)
returning id;
