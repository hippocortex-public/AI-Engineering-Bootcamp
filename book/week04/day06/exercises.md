# Exercices

## Exercice 1 — Identifier les signaux

Pour chaque élément, indique s'il s'agit d'un log, d'un event, d'une metric, d'un span ou d'une trace.

1. `support_agent_run`
2. `tool.search_ticket`
3. `schema_validation_failed`
4. `agent.run.duration_ms = 842`
5. `INFO tool called`

## Exercice 2 — Concevoir une trace

On veut instrumenter un agent qui :

1. reçoit une demande client ;
2. classe l'intention ;
3. lit la mémoire utilisateur ;
4. appelle un outil de recherche ;
5. génère une réponse finale.

Dessine l'arbre de spans attendu.

## Exercice 3 — Redaction

Explique pourquoi les attributs suivants doivent être masqués par défaut :

```json
{
  "email": "client@example.com",
  "api_key": "sk-...",
  "ticket_id": "TCK-1001"
}
```

Indique lesquels peuvent rester visibles.

## Exercice 4 — Statut d'échec

Un outil échoue, mais l'agent produit une réponse de secours.

Réponds :

1. le span outil doit-il être `failed` ?
2. la trace complète doit-elle forcément être `failed` ?
3. quelle information doit apparaître dans le rapport de santé ?

## Exercice 5 — Métriques

Propose cinq métriques utiles pour suivre un mini-framework d'agents.

Pour chaque métrique, indique :

- son nom ;
- son unité ;
- pourquoi elle est utile.

## Exercice 6 — Implémentation

Dans le lab, ajoute un événement `guardrail_blocked` lorsqu'un outil sensible est refusé.

Critères :

- l'événement doit être rattaché au span courant ;
- les attributs sensibles doivent être redacted ;
- l'export JSON doit contenir cet événement.

## Exercice 7 — Analyse d'export

À partir d'un export JSON, écris une fonction qui retourne :

- le nombre de traces ;
- le nombre de spans en échec ;
- le nombre d'événements `error`;
- la durée moyenne des spans terminés.
