# Lab — PostgreSQL AI Persistence

## Objectif

Construire une couche de persistance pour assistant IA avec PostgreSQL comme source durable.

Le lab contient :

- un schéma PostgreSQL ;
- des index ;
- des données de seed ;
- un modèle métier Python ;
- un contrat de repository ;
- un adaptateur mémoire testable ;
- un squelette d’adaptateur PostgreSQL ;
- des tests unitaires exécutables sans base externe.

## Pourquoi un adaptateur mémoire ?

L’adaptateur mémoire permet de tester la logique de conversation sans dépendre d’un serveur PostgreSQL. Ce n’est pas un remplacement de PostgreSQL en production. C’est un outil de test.

## Installation locale

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m unittest discover -s tests
```

## Lancer PostgreSQL avec Docker

```bash
docker compose up -d
```

Appliquer le schéma :

```bash
psql postgresql://bootcamp:bootcamp@localhost:5432/ai_bootcamp -f sql/001_schema.sql
psql postgresql://bootcamp:bootcamp@localhost:5432/ai_bootcamp -f sql/002_indexes.sql
psql postgresql://bootcamp:bootcamp@localhost:5432/ai_bootcamp -f sql/003_seed.sql
```

## Structure

```text
postgresql_ai_persistence/
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── sql/
├── src/
└── tests/
```

## Exercices pratiques

1. Lire `sql/001_schema.sql`.
2. Identifier les contraintes `CHECK`.
3. Expliquer les index de `sql/002_indexes.sql`.
4. Exécuter les tests.
5. Ajouter une méthode `list_failed_runs`.
6. Ajouter une clé d’idempotence sur les messages.
