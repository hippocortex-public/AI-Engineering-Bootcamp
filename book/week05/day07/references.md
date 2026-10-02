# Références — Déploiement

## Sources primaires consultées le 2 octobre 2026

- Docker, ordre de démarrage : https://docs.docker.com/compose/how-tos/startup-order/
- Docker, production Compose : https://docs.docker.com/compose/how-tos/production/
- Docker, services : https://docs.docker.com/reference/compose-file/services/
- Docker, secrets : https://docs.docker.com/reference/compose-file/secrets/
- FastAPI, conteneurs : https://fastapi.tiangolo.com/deployment/docker/
- Redis, INCR et script atomique : https://redis.io/docs/latest/commands/incr/
- PostgreSQL 16, psql et getenv : https://www.postgresql.org/docs/16/app-psql.html

## Raccordement interne

J2 : API et validation. J3 : cache et TTL. J4 : requêtes et persistance.
J5 : métriques et diagnostic. J6 : identité, tenant, secrets et limites.
Le J7 reprend ces principes dans une stack déployable autonome.
