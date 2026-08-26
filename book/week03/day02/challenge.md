# Challenge — Coordinateur multi-agent contrôlé

## Contexte

Tu construis le moteur de coordination d'un assistant IA interne pour une équipe SaaS.

L'assistant peut déléguer à plusieurs agents :

- `support_agent` ;
- `billing_agent` ;
- `engineering_agent` ;
- `security_agent` ;
- `product_agent` ;
- `reviewer_agent`.

L'objectif est de produire une réponse finale fiable à partir d'une demande utilisateur.

## Mission

Améliore le lab pour supporter un workflow de coordination complet.

## Exigences fonctionnelles

Le coordinateur doit :

1. recevoir une tâche structurée ;
2. sélectionner les agents utiles ;
3. construire un plan d'exécution ;
4. exécuter les agents sélectionnés ;
5. collecter les observations ;
6. détecter les conflits ;
7. déclencher une revue si nécessaire ;
8. générer une réponse finale ;
9. produire une trace JSON.

## Règles de coordination

Le reviewer doit être déclenché si :

- le risque est `high` ;
- au moins un conflit est détecté ;
- la tâche contient le domaine `security` ;
- la réponse finale contient une action sensible ;
- aucun agent spécialiste n'a été sélectionné.

## Règles de contexte

Chaque agent ne doit recevoir que :

- l'identifiant de tâche ;
- l'objectif ;
- les domaines liés à sa compétence ;
- le niveau de risque ;
- les contraintes utiles.

## Règles de sortie

La sortie finale doit contenir :

```json
{
  "task_id": "string",
  "status": "completed | needs_review | needs_clarification",
  "selected_agents": ["string"],
  "review_performed": true,
  "conflicts": ["string"],
  "final_answer": "string",
  "trace": []
}
```

## Contraintes techniques

- Ne pas utiliser de dépendance externe.
- Ne pas appeler d'API.
- Garder le code testable avec `python test_multi_agent_coordinator.py`.
- Les décisions doivent être déterministes.
- Le code doit rester lisible.

## Bonus

Ajoute une politique de quorum :

- si trois agents ou plus sont sélectionnés ;
- et si deux agents convergent sur un statut identique ;
- le coordinateur peut produire une synthèse plus confiante ;
- sauf si `security_agent` ou `reviewer_agent` signale un blocage.
