# Corrigé — Exercices MCP Server

## Exercice 1 — Classification

| Élément | Catégorie | Justification |
|---|---|---|
| `lookup_order` | Tool | Action invocable qui interroge un système métier |
| `support_policy_refunds` | Resource | Document ou donnée consultable |
| `triage_customer_message_template` | Prompt | Gabarit d’instruction réutilisable |
| `refund_order` | Tool | Action métier avec effet financier |
| `product_catalog_readonly` | Resource | Donnée consultable en lecture seule |
| `create_support_draft` | Tool | Action de génération contrôlée côté serveur |

## Exercice 2 — Schéma

```json
{
  "type": "object",
  "properties": {
    "customer_message": {
      "type": "string",
      "minLength": 1
    },
    "tone": {
      "type": "string",
      "enum": ["professional", "friendly", "concise"]
    },
    "language": {
      "type": "string",
      "enum": ["fr", "en"]
    }
  },
  "required": ["customer_message", "tone", "language"],
  "additionalProperties": false
}
```

## Exercice 3 — Erreur

La requête doit être refusée parce que `lookup_order` exige `order_id`.

Le code approprié est `-32602`, généralement utilisé pour `Invalid params`.

`error.data` doit indiquer :

```json
{
  "field": "order_id",
  "reason": "required"
}
```

## Exercice 4 — Garde-fous

Trois garde-fous utiles :

1. Exiger `approved_by_human=true`.
2. Imposer un plafond de montant.
3. Vérifier l’état de la commande et l’éligibilité au remboursement.

On pourrait aussi tracer l’identité de l’approbateur, limiter par rôle et imposer une idempotence.

## Exercice 5 — Resource

Exemple :

```python
server.register_resource(ResourceDefinition(
    uri="kb://support/escalation",
    name="Escalation policy",
    mime_type="text/markdown",
    text="Escalate when the customer reports legal risk, payment failure, repeated SLA breach, or safety concern."
))
```

Test attendu :

```python
response = server.handle({
    "jsonrpc": "2.0",
    "id": "res-1",
    "method": "resources/read",
    "params": {"uri": "kb://support/escalation"}
})
assert response["result"]["contents"][0]["uri"] == "kb://support/escalation"
```

## Exercice 6 — Trace

Une trace minimale :

```python
{
    "request_id": "req-1",
    "method": "tools/call",
    "status": "error",
    "tool_name": "lookup_order",
    "error_code": -32602
}
```

## Exercice 7 — Réponse attendue

Un serveur MCP est préférable à un accès direct aux fonctions Python car il crée une frontière d’architecture. Cette frontière permet au modèle de découvrir des capacités sans connaître l’implémentation interne. Elle force la description des entrées, la validation, la gestion d’erreurs, la traçabilité et les politiques de sécurité. Elle permet aussi de réutiliser les mêmes capacités depuis plusieurs clients. En production, cette séparation évite que l’agent dépende du code interne de l’application. Elle facilite les tests, la gouvernance, le versioning et l’audit. Enfin, elle permet de désactiver ou de restreindre un outil sans modifier le raisonnement de l’agent.
