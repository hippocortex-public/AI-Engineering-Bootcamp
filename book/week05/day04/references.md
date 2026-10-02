# Références — Semaine 5 Jour 4

## Documentation principale

- PostgreSQL Documentation — SQL, types, index et transactions.
- PostgreSQL Documentation — `jsonb` data type.
- PostgreSQL Documentation — constraints.
- PostgreSQL Documentation — indexing.
- PostgreSQL Documentation — transaction isolation.
- Psycopg Documentation — PostgreSQL adapter for Python.
- SQLAlchemy Documentation — Core and ORM patterns.
- FastAPI Documentation — dependency injection and database sessions.

## Concepts à maîtriser

- ACID ;
- transaction ;
- clé primaire ;
- clé étrangère ;
- index composite ;
- contrainte `CHECK` ;
- `JSONB` ;
- migration de schéma ;
- repository pattern ;
- idempotence ;
- audit trail ;
- multi-tenancy.

## Lectures recommandées

1. Concevoir un schéma à partir des requêtes de production.
2. Séparer données volatiles et données durables.
3. Ne pas remplacer le modèle relationnel par un document JSON global.
4. Tester la logique métier sans dépendre d’une base externe.
5. Préparer l’observabilité dès le schéma de données.

## Pour aller plus loin

- Étudier les migrations avec Alembic.
- Ajouter un pool de connexions.
- Implémenter Row Level Security pour le multi-tenant.
- Ajouter des politiques de rétention.
- Brancher les événements persistés sur un pipeline d’évaluation.
