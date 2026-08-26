# Lab — Projet multi-agent

## Objectif

Ce lab construit un projet multi-agent complet en Python standard library.

Il simule :

- un coordinateur ;
- plusieurs agents spécialisés ;
- un adaptateur MCP ;
- un état partagé versionné ;
- un context builder ;
- une revue finale ;
- une trace JSON.

## Fichiers

```text
labs/
├── multi_agent_project.py
└── test_multi_agent_project.py
```

## Exécution

Depuis ce dossier :

```bash
python multi_agent_project.py
python test_multi_agent_project.py
```

## Dépendances

Aucune dépendance externe n’est requise.

## Points à observer

Pendant la lecture du code, identifiez :

- où l’objectif est validé ;
- où le plan est créé ;
- où le contexte est filtré ;
- où les outils sont validés ;
- où les actions sensibles sont bloquées ;
- où l’état est versionné ;
- où la revue finale décide le statut.
