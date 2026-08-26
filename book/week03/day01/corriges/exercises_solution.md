# Corrigé — Exercices

## Exercice 1

1. **Router / triage** : il faut choisir le bon domaine.
2. **Manager-worker** : le manager agrège plusieurs analyses.
3. **Reviewer** : il vérifie la conformité d’une réponse.
4. **Handoff** : le spécialiste doit prendre le contrôle.
5. **Parallèle** : les analyses sont indépendantes.

## Exercice 2

Architecture possible :

```text
User → Triage Agent
        ├── Billing Specialist
        ├── Technical Specialist
        ├── Product Specialist
        ├── Security Specialist
        └── Cancellation Specialist
              ↓
           Reviewer Agent
              ↓
          Final Answer
```

Responsabilités :

- `triage_agent` : classer la demande et choisir l’agent cible.
- `billing_specialist` : factures, paiements, abonnements.
- `technical_specialist` : bugs, incidents, logs.
- `product_specialist` : demandes de fonctionnalités.
- `security_specialist` : accès, permissions, conformité.
- `cancellation_specialist` : résiliation.
- `reviewer_agent` : vérifier format, ton, limites et sécurité.

## Exercice 3

```json
{
  "agent_name": "security_specialist",
  "responsibility": "Analyze security-related customer requests and produce a safe support answer.",
  "input_schema": {
    "ticket_id": "string",
    "customer_message": "string",
    "account_context": "object"
  },
  "output_schema": {
    "category": "security",
    "answer": "string",
    "risk_level": "low|medium|high",
    "requires_human_review": "boolean"
  },
  "allowed_tools": [
    "get_security_policy",
    "get_account_security_events"
  ],
  "handoff_conditions": [
    "legal_request",
    "suspected_data_breach",
    "law_enforcement_request"
  ],
  "failure_modes": [
    "missing_account_context",
    "insufficient_authorization",
    "ambiguous_security_request"
  ]
}
```

## Exercice 4

| Élément | Classification |
|---|---|
| Message utilisateur courant | Toujours partagé |
| Historique complet | Partagé sous condition |
| Décision de routage | Toujours partagé |
| Mémoire long terme | Partagé sous condition stricte |
| Résultat intermédiaire | Partagé sous condition |
| Données sensibles | Partagé sous condition stricte |
| Trace d’exécution | Toujours partagé côté système |
| Raisonnement interne | Jamais partagé |

## Exercice 5

- FAQ simple : coût et latence inutiles.
- Tâche mono-domaine : routage sans bénéfice.
- Rôles flous : réponses contradictoires et responsabilités diluées.

## Exercice 6

Une bonne extension ajoute un agent `security`, ses mots-clés et un test déterministe. Le test ne doit pas dépendre d’un appel LLM réel.
