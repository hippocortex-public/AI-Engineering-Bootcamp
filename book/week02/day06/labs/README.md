# Lab — Agent Loop & planification

## Objectif

Implémenter et tester une boucle agentique déterministe.

Le lab ne dépend pas d'une API externe. Il simule les décisions qui pourraient être produites par un LLM, afin de tester l'architecture.

## Fichiers

```text
labs/
├── agent_loop_planner.py
└── test_agent_loop_planner.py
```

## Exécution

Depuis ce dossier :

```bash
python agent_loop_planner.py
python test_agent_loop_planner.py
```

## Compétences travaillées

- État explicite
- Planification
- Replanification
- Tool registry
- Observation
- Reducer
- Condition d'arrêt
- Journalisation
- Tests déterministes

## Résultat attendu

Les tests doivent passer et l'exécution doit afficher une réponse finale de support.
