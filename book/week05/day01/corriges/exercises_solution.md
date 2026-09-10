# Corrigé — Exercices

## Exercice 1

### Architecture A

Catégorie : `prototype`.

Risques : pas de backend, pas de state robuste, pas de traçabilité, pas de contrôle de coût, pas de sécurité production.

Amélioration minimale : ajouter API backend, service applicatif, model gateway, validation et observabilité.

### Architecture B

Catégorie : `pré-production` ou `production` selon les détails.

Points forts : séparation API/runtime, gateway modèle, gateway outils, observabilité et state store.

Manques possibles : memory store, business database, policy de sécurité, rollback, evals et gestion des secrets.

### Architecture C

Catégorie : `prototype automatisé`.

Risques : envoi automatique non contrôlé, absence d’idempotence, pas de validation humaine, pas d’observabilité, coût non borné.

Amélioration minimale : passer en mode draft, ajouter queue, validation humaine, idempotency key et audit log.

## Exercice 2

| Composant | Responsabilité |
|---|---|
| API | Authentifier, valider, exposer le cas d’usage |
| Application Service | Orchestrer le cas support |
| Agent Runtime | Exécuter l’agent dans des limites contrôlées |
| Model Gateway | Encapsuler modèle, retry, timeout, coût |
| Tool Gateway | Protéger les outils internes |
| State Store | Stocker l’état court terme |
| Memory Store | Stocker les préférences durables |
| Business DB | Stocker tickets, clients, remboursements |
| Observability | Tracer appels, erreurs, coûts, latences |
| Guardrails | Empêcher sorties ou actions non conformes |

## Exercice 3

| Élément | Catégorie |
|---|---|
| Dernier message utilisateur | conversation state |
| Préférence “réponds en français” | memory |
| Numéro de commande | business database ou state si temporaire |
| Trace d’un appel outil | observability |
| `waiting_for_human_approval` | conversation state |
| Historique des remboursements | business database |
| Latence d’un appel modèle | observability |
| Slot `ticket_id` | conversation state |

## Exercice 4

Checklist proposée :

- Authentification active.
- Autorisation par rôle.
- Rate limiting.
- Validation d’entrée.
- Structured outputs validés.
- Outils sensibles protégés.
- Validation humaine pour remboursement.
- State store isolé par session.
- Memory store gouverné.
- Logs sans PII.
- Traces disponibles.
- Métriques de latence.
- Métriques de coût.
- Timeouts configurés.
- Retry borné.
- Fallback défini.
- Prompts versionnés.
- Schémas versionnés.
- Rollback documenté.
- Evals minimales passées.

## Exercice 5

```json
{
  "name": "support-ai-platform",
  "components": [
    {"name": "api", "kind": "api", "critical": true},
    {"name": "auth", "kind": "security", "critical": true},
    {"name": "support_service", "kind": "application_service", "critical": true},
    {"name": "agent_runtime", "kind": "agent_runtime", "critical": true},
    {"name": "model_gateway", "kind": "model_gateway", "critical": true},
    {"name": "tool_gateway", "kind": "tool_gateway", "critical": true},
    {"name": "state_store", "kind": "state_store", "critical": true},
    {"name": "memory_store", "kind": "memory_store", "critical": true},
    {"name": "business_db", "kind": "business_database", "critical": true},
    {"name": "observability", "kind": "observability", "critical": true}
  ],
  "controls": [
    "authentication",
    "authorization",
    "rate_limiting",
    "timeouts",
    "bounded_retries",
    "structured_outputs",
    "human_approval",
    "pii_redaction",
    "cost_budget",
    "trace_export",
    "rollback_plan"
  ],
  "risks": [
    "hallucination",
    "tool_misuse",
    "pii_leakage",
    "cost_spike"
  ]
}
```
