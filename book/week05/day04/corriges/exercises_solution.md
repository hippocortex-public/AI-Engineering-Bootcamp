# Corrigé — Exercices Semaine 5 Jour 4

## Exercice 1 — Répartition Redis / PostgreSQL

| Donnée | Redis | PostgreSQL | Justification |
|---|---:|---:|---|
| Rate limit utilisateur | Oui | Non | Compteur temporaire avec expiration. |
| Message utilisateur | Non prioritaire | Oui | Donnée durable nécessaire à l’historique et à l’audit. |
| Réponse assistant finale | Non prioritaire | Oui | Doit pouvoir être reconstruite et analysée. |
| Résultat temporaire de streaming | Oui | Non | Etat volatil lié à une connexion active. |
| Run agent échoué | Non | Oui | Indispensable pour debug, monitoring et audit. |
| Session courte d’interface | Oui | Optionnel | Expiration naturelle et accès rapide. |
| Evaluation de qualité | Non | Oui | Signal analytique durable. |
| Cache d’un appel outil | Oui | Optionnel | Redis pour accélérer ; PostgreSQL seulement si le résultat doit être audité. |

## Exercice 2 — Schéma relationnel

Schéma minimal :

```sql
create table conversations (
    id uuid primary key,
    tenant_id text not null,
    user_id text not null,
    title text not null,
    status text not null check (status in ('active', 'archived')),
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table messages (
    id uuid primary key,
    conversation_id uuid not null references conversations(id) on delete cascade,
    role text not null check (role in ('system', 'user', 'assistant', 'tool')),
    content text not null,
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create table agent_runs (
    id uuid primary key,
    conversation_id uuid not null references conversations(id) on delete cascade,
    status text not null check (status in ('pending', 'running', 'succeeded', 'failed')),
    model text not null,
    prompt_version text not null,
    input_tokens integer not null default 0 check (input_tokens >= 0),
    output_tokens integer not null default 0 check (output_tokens >= 0),
    latency_ms integer check (latency_ms is null or latency_ms >= 0),
    error_message text,
    started_at timestamptz not null default now(),
    finished_at timestamptz
);

create table tool_calls (
    id uuid primary key,
    agent_run_id uuid not null references agent_runs(id) on delete cascade,
    tool_name text not null,
    arguments jsonb not null default '{}'::jsonb,
    result jsonb,
    status text not null check (status in ('pending', 'running', 'succeeded', 'failed')),
    latency_ms integer check (latency_ms is null or latency_ms >= 0),
    created_at timestamptz not null default now()
);
```

## Exercice 3 — Transaction de tour conversationnel

Transaction recommandée :

```text
BEGIN
  insert message utilisateur
  insert agent_run status='running'
  exécuter logique agent
  insert tool_calls éventuels
  insert message assistant
  update agent_run status='succeeded'
COMMIT
```

En cas d’erreur après l’appel LLM mais avant l’écriture du message assistant, deux stratégies sont possibles :

1. **Rollback total** : aucune trace partielle n’est conservée. Simple, mais moins utile pour debug.
2. **Transaction contrôlée avec statut failed** : le message utilisateur et le run sont conservés, puis le run est marqué `failed` avec `error_message`. Plus utile en production.

La deuxième stratégie est généralement préférable pour un système IA, car les échecs doivent être observables.

## Exercice 4 — Indexation

### Requête A

```sql
create index if not exists idx_conversations_tenant_user_created
on conversations (tenant_id, user_id, created_at desc);
```

### Requête B

```sql
create index if not exists idx_messages_conversation_created
on messages (conversation_id, created_at asc);
```

### Requête C

```sql
create index if not exists idx_agent_runs_status_started
on agent_runs (status, started_at desc);
```

### Requête D

```sql
create index if not exists idx_agent_runs_status_model
on agent_runs (status, model);
```

L’index D aide le filtre par `status` et le regroupement par `model`.

## Exercice 5 — Repository testable

```python
from typing import Protocol

class ConversationStore(Protocol):
    def create_conversation(self, tenant_id: str, user_id: str, title: str):
        ...

    def append_message(self, conversation_id: str, role: str, content: str):
        ...

    def list_messages(self, conversation_id: str):
        ...
```

Un adaptateur mémoire permet de tester la logique métier sans serveur PostgreSQL. Il rend les tests rapides, déterministes et indépendants de l’infrastructure.

## Exercice 6 — JSONB ou colonne dédiée ?

| Champ | Colonne | JSONB | Justification |
|---|---:|---:|---|
| `conversation_id` | Oui | Non | Relation centrale, souvent filtrée. |
| `role` du message | Oui | Non | Valeur contrôlée par contrainte. |
| `temperature` du modèle | Optionnel | Oui | Paramètre variable selon provider ou expérience. |
| `request_id` externe | Optionnel | Oui ou colonne si souvent recherché | Devient colonne si utilisé pour idempotence. |
| `created_at` | Oui | Non | Dimension temporelle critique. |
| `safety_profile` | Optionnel | Oui | Métadonnée évolutive. |
| `status` du run | Oui | Non | Filtre opérationnel fréquent. |
| `tool_arguments` | Non | Oui | Structure variable selon outil. |
