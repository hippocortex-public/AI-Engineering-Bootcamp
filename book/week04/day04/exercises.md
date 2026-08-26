# Exercices

## Exercice 1 — Classifier les mémoires

Classe les exemples suivants dans une catégorie :

- `conversation`
- `preference`
- `fact`
- `task_state`
- `tool_observation`
- `policy`

Exemples :

1. "L'utilisateur préfère les réponses en tableau."
2. "Le paiement a échoué avec le code 402."
3. "La tâche courante attend une validation humaine."
4. "Ne jamais appeler l'outil delete sans confirmation."
5. "User: peux-tu continuer ?"
6. "Le projet utilise un mini-framework maison."

## Exercice 2 — Concevoir un record mémoire

Écris un record JSON pour mémoriser la préférence suivante :

> "L'utilisateur préfère recevoir les explications sous forme d'étapes numérotées."

Contraintes :

- namespace : `user:42`
- owner_agent : `planner`
- kind approprié
- visibilité privée
- importance élevée
- tags utiles

## Exercice 3 — Filtrer le contexte

Tu reçois ces mémoires :

```json
[
  {"content": "Préférence privée", "visibility": "private"},
  {"content": "Fait partagé", "visibility": "shared"},
  {"content": "Annonce publique", "visibility": "public"}
]
```

Un agent non propriétaire ne peut lire que `shared` et `public`.

Quelles mémoires peuvent être injectées ?

## Exercice 4 — TTL

Explique pourquoi une mémoire de type `task_state` devrait souvent avoir un TTL, alors qu'une préférence utilisateur peut ne pas en avoir.

## Exercice 5 — Fonction de retrieval

Propose une fonction de scoring simple basée sur :

- overlap lexical ;
- tags ;
- importance.

L'objectif est l'explicabilité, pas la performance maximale.

## Exercice 6 — Droit à l'oubli

Décris ce que doit faire `forget_namespace("user:42")`.

## Exercice 7 — Tests nécessaires

Liste cinq tests unitaires indispensables pour une Memory Layer.
