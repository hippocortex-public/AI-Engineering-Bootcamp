# Corrigé — Challenge

## Architecture proposée

L'assistant autonome mono-agent peut être structuré autour des composants suivants :

```text
AutonomousSupportAgent
├── ToolRegistry
├── AgentState
├── Task
├── TraceEvent
└── Guardrails
```

## Règles principales

1. Une demande de remboursement sans `order_id` passe en `needs_input`.
2. L'outil de remboursement est sensible.
3. Une action sensible nécessite une approbation explicite.
4. Le nombre d'étapes est limité.
5. Le budget est limité.
6. Chaque étape produit une trace.

## Exemple de plan remboursement

```json
[
  {
    "id": "T1",
    "name": "Lire la politique de remboursement",
    "tool_name": "search_refund_policy",
    "status": "pending"
  },
  {
    "id": "T2",
    "name": "Vérifier la commande",
    "tool_name": "check_order",
    "arguments": {
      "order_id": "ORDER-1234"
    },
    "status": "pending"
  },
  {
    "id": "T3",
    "name": "Créer un ticket de suivi",
    "tool_name": "create_support_ticket",
    "arguments": {
      "order_id": "ORDER-1234",
      "reason": "refund_request"
    },
    "status": "pending"
  },
  {
    "id": "T4",
    "name": "Préparer un remboursement potentiel",
    "tool_name": "issue_refund",
    "requires_approval": true,
    "status": "pending"
  },
  {
    "id": "T5",
    "name": "Rédiger la réponse finale",
    "tool_name": "draft_response",
    "status": "pending"
  }
]
```

## Tests minimaux

Le lab fourni contient les tests suivants :

- extraction d'un identifiant de commande ;
- demande de remboursement sans identifiant ;
- création du plan de remboursement ;
- blocage d'une action sensible sans approbation ;
- complétion avec approbation ;
- respect de `max_steps` ;
- respect de `max_budget` ;
- sérialisation de l'état ;
- rejet d'un outil inconnu ;
- présence des traces principales.

## Propositions d'amélioration

Ajouter un champ `risk_level` peut améliorer la lisibilité :

```python
risk_level: Literal["low", "medium", "high"]
```

Règle associée :

```text
Toute tâche high nécessite une approbation humaine.
```

Cette amélioration ne modifie pas la structure du projet. Elle enrichit seulement le modèle métier du lab.
