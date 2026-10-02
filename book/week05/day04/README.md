# Semaine 5 — Jour 4 : PostgreSQL pour systèmes IA en production

## Position dans le bootcamp

La semaine 5 traite des **systèmes IA en production**. Après l’architecture de production, l’API FastAPI et Redis, ce jour introduit PostgreSQL comme couche de persistance durable pour les applications IA.

Redis répond aux besoins de cache, de sessions courtes et d’état volatil. PostgreSQL répond aux besoins de **durabilité**, de **cohérence**, de **traçabilité**, d’**audit** et de **requêtage analytique**.

## Objectif du jour

Concevoir et implémenter une couche PostgreSQL capable de stocker les éléments critiques d’un système IA :

- conversations ;
- messages utilisateur et assistant ;
- appels d’outils ;
- exécutions d’agents ;
- métadonnées JSON ;
- traces d’évaluation ;
- statuts d’exécution ;
- événements auditables.

## Compétence visée

À la fin de la journée, l’apprenant sait expliquer et construire une base PostgreSQL pour une plateforme IA en production, avec un schéma robuste, des transactions contrôlées, des index utiles et une interface de repository testable.

## Livrables produits

```text
book/week05/day04/
├── README.md
├── learning_objectives.md
├── chapter.md
├── exercises.md
├── interview.md
├── challenge.md
├── references.md
├── corriges/
│   ├── exercises_solution.md
│   ├── interview_solution.md
│   ├── challenge_solution.md
│   └── review.md
├── diagrams/
│   ├── persistence_architecture.mmd
│   ├── schema_overview.mmd
│   └── transaction_flow.mmd
├── assets/
│   └── README.md
└── labs/
    └── postgresql_ai_persistence/
        ├── README.md
        ├── docker-compose.yml
        ├── pyproject.toml
        ├── requirements.txt
        ├── sql/
        │   ├── 001_schema.sql
        │   ├── 002_indexes.sql
        │   └── 003_seed.sql
        ├── src/
        │   └── ai_persistence/
        │       ├── __init__.py
        │       ├── domain.py
        │       ├── repository.py
        │       └── sql_builder.py
        └── tests/
            ├── test_domain.py
            ├── test_repository_contract.py
            └── test_sql_builder.py
```

## Notebooks générés

```text
notebooks/week05/S5_J4_postgresql.ipynb
notebooks/week05/teacher/S5_J4_postgresql_teacher.ipynb
```

Le notebook étudiant exclut les corrigés. Le notebook enseignant inclut les solutions et les notes de revue.

## Projet pratique

Le lab construit une couche de persistance appelée `ai_persistence`. Elle expose :

- un modèle métier typé ;
- un contrat de repository ;
- un adaptateur mémoire pour les tests ;
- un squelette PostgreSQL prêt à connecter ;
- des scripts SQL de schéma, index et seed ;
- une suite de tests exécutable sans serveur PostgreSQL.

## Commandes principales

Depuis le dossier du lab :

```bash
python -m unittest discover -s tests
python -m compileall src tests
```

Avec Docker disponible :

```bash
docker compose up -d
psql postgresql://bootcamp:bootcamp@localhost:5432/ai_bootcamp -f sql/001_schema.sql
psql postgresql://bootcamp:bootcamp@localhost:5432/ai_bootcamp -f sql/002_indexes.sql
psql postgresql://bootcamp:bootcamp@localhost:5432/ai_bootcamp -f sql/003_seed.sql
```

## Résultat attendu

L’apprenant doit être capable de justifier :

1. pourquoi PostgreSQL est utilisé pour la persistance durable ;
2. ce qui doit rester dans Redis ;
3. comment structurer les tables d’un système IA ;
4. comment préserver l’intégrité des traces agentiques ;
5. comment préparer le monitoring, l’audit et l’évaluation à partir des données persistées.
