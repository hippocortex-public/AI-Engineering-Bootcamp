# Corrigé — Exercices

## Exercice 1

1. `support_agent_run` : trace.
2. `tool.search_ticket` : span.
3. `schema_validation_failed` : event.
4. `agent.run.duration_ms = 842` : metric.
5. `INFO tool called` : log.

## Exercice 2

Arbre possible :

```text
support_agent_run
├── classify_intent
├── memory.retrieve_user_profile
├── tool.search_ticket
└── final_answer
```

Version plus détaillée :

```text
support_agent_run
├── agent.classify_intent
├── memory.retrieve_user_profile
│   └── event: memory_hits
├── tool.search_ticket
│   ├── event: arguments_validated
│   └── metric: tool.duration_ms
└── agent.final_answer
```

## Exercice 3

`email` et `api_key` doivent être masqués. `ticket_id` peut rester visible si la politique de l'organisation l'autorise et s'il ne permet pas seul d'identifier une personne.

Exemple redacted :

```json
{
  "email": "[REDACTED]",
  "api_key": "[REDACTED]",
  "ticket_id": "TCK-1001"
}
```

## Exercice 4

1. Oui, le span outil doit être `failed`.
2. Non, la trace complète peut être `completed` si l'agent a géré l'échec correctement.
3. Le rapport doit mentionner le span en échec, l'erreur, et le fallback utilisé.

## Exercice 5

Métriques possibles :

| Nom | Unité | Utilité |
|---|---:|---|
| `agent.run.duration_ms` | ms | suivre la latence globale |
| `tool.call.count` | count | suivre l'activité d'outillage |
| `tool.error.count` | count | détecter les outils instables |
| `guardrail.blocked.count` | count | suivre les actions refusées |
| `workflow.retry.count` | count | détecter la fragilité d'un workflow |

## Exercice 6

Solution conceptuelle :

```python
with obs.start_span("tool.delete_ticket", kind="tool"):
    obs.record_event(
        "guardrail_blocked",
        "Sensitive tool blocked without human approval",
        level="warning",
        attributes={"tool": "delete_ticket", "user_email": "client@example.com"},
    )
```

L'export doit contenir `user_email: "[REDACTED]"`.

## Exercice 7

Pseudo-code :

```python
def summarize_export(payload):
    spans = payload["spans"]
    failed_spans = [s for s in spans if s["status"] == "failed"]
    error_events = [e for e in payload["events"] if e["level"] == "error"]
    durations = [s["duration_ms"] for s in spans if s["duration_ms"] is not None]
    return {
        "trace_count": len(payload["traces"]),
        "failed_span_count": len(failed_spans),
        "error_event_count": len(error_events),
        "avg_duration_ms": sum(durations) / len(durations) if durations else 0,
    }
```
