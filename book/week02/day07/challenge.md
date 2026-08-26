# Challenge — Assistant autonome mono-agent

## Objectif

Construire un assistant autonome mono-agent pour un cas de support client.

L'assistant doit traiter au moins trois types de demandes :

1. remboursement ;
2. création de ticket ;
3. demande incomplète.

## Contraintes

L'agent doit :

- créer un plan explicite ;
- appeler des outils via un registre ;
- conserver un état sérialisable ;
- produire des traces ;
- demander une validation humaine pour les actions sensibles ;
- respecter `max_steps` ;
- respecter `max_budget` ;
- produire une réponse finale ;
- être testé.

## Outils minimaux

Implémente au moins les outils suivants :

- `check_order`;
- `search_policy`;
- `create_ticket`;
- `issue_refund`;
- `draft_response`.

## Scénarios à tester

### Scénario 1 — Remboursement avec approbation

Entrée :

```text
Je veux un remboursement pour ORDER-1234.
```

Résultat attendu :

- plan créé ;
- commande vérifiée ;
- ticket créé ;
- remboursement exécuté seulement si approbation ;
- réponse finale produite.

### Scénario 2 — Remboursement sans identifiant de commande

Entrée :

```text
Je veux un remboursement.
```

Résultat attendu :

- statut `needs_input` ;
- champ manquant `order_id` ;
- aucun outil exécuté.

### Scénario 3 — Ticket support

Entrée :

```text
Créer un ticket support.
```

Résultat attendu :

- ticket créé ;
- réponse finale produite ;
- aucun outil sensible appelé.

### Scénario 4 — Budget insuffisant

Entrée :

```text
Je veux un remboursement pour ORDER-1234.
```

Configuration :

```text
max_budget = 1
```

Résultat attendu :

- l'agent s'arrête ;
- une trace explique l'arrêt ;
- aucune action sensible n'est exécutée.

## Extension facultative

Ajoute un champ `risk_level` sur chaque tâche :

```text
low | medium | high
```

Puis impose que toute tâche `high` demande une validation humaine.
