# Corrigé — Challenge

## 1. Arbre de spans

```text
support_agent_run
├── agent.classify_request
├── memory.retrieve_profile
├── tool.search_ticket
├── agent.propose_action
├── guardrail.require_approval
└── agent.final_response
```

## 2. Événements

| Event | Niveau | Span |
|---|---|---|
| `intent_classified` | info | `agent.classify_request` |
| `pii_redacted` | info | `memory.retrieve_profile` |
| `tool_arguments_validated` | info | `tool.search_ticket` |
| `sensitive_action_detected` | warning | `guardrail.require_approval` |
| `human_approval_required` | warning | `guardrail.require_approval` |
| `fallback_response_used` | warning | `agent.final_response` |

## 3. Métriques

| Metric | Unité |
|---|---:|
| `support.run.duration_ms` | ms |
| `support.tool.count` | count |
| `support.guardrail.blocked.count` | count |
| `support.memory.hit.count` | count |
| `support.error.count` | count |

## 4. Redaction

Règles :

- masquer `email`, `phone`, `api_key`, `token`, `secret`, `password` ;
- ne stocker que les IDs métier autorisés ;
- ne pas stocker le prompt complet ;
- résumer les résultats outil.

## 5. Statuts

| Élément | Statuts possibles |
|---|---|
| trace | `running`, `completed`, `failed` |
| span | `running`, `completed`, `failed` |
| action sensible | `allowed`, `blocked`, `requires_approval` |

## 6. Exemple d'export JSON

```json
{
  "traces": [
    {
      "trace_id": "trace_001",
      "name": "support_agent_run",
      "status": "completed"
    }
  ],
  "spans": [
    {
      "span_id": "span_001",
      "trace_id": "trace_001",
      "name": "tool.search_ticket",
      "kind": "tool",
      "status": "completed",
      "attributes": {
        "email": "[REDACTED]",
        "ticket_id": "TCK-1001"
      }
    }
  ],
  "events": [
    {
      "name": "human_approval_required",
      "level": "warning"
    }
  ],
  "metrics": [
    {
      "name": "support.tool.count",
      "value": 1,
      "unit": "count"
    }
  ]
}
```

## 7. Alertes opérationnelles

1. taux d'échec outil > 5 % sur 10 minutes ;
2. latence P95 d'une trace > 5 secondes ;
3. hausse du nombre d'actions bloquées par guardrail.

## Conclusion

La trace complète peut être `completed` même si une action sensible a été bloquée, à condition que l'agent ait produit une réponse sûre et explicite.
