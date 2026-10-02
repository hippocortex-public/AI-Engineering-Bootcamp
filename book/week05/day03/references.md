# Références

## Documentation technique à consulter

- Redis documentation — commandes `GET`, `SET`, `INCR`, `EXPIRE`, structures de données et TTL.
- redis-py documentation — client Python asynchrone `redis.asyncio`.
- FastAPI documentation — dépendances, endpoints asynchrones et gestion des erreurs HTTP.
- Docker Compose documentation — orchestration locale d'un service Redis et d'une API.
- OWASP Cheat Sheet Series — stockage de données sensibles, logs et secrets.

## Concepts à maîtriser

- Cache-aside pattern.
- TTL et invalidation de cache.
- Rate limiting par fenêtre fixe.
- Idempotency key.
- Session state court terme.
- Différence entre stockage volatil et stockage durable.
- Dégradation contrôlée d'un service de production.

## Pour aller plus loin

- Fenêtre glissante avec sorted sets Redis.
- Redis Streams pour pipelines d'événements.
- Redis Sentinel et Redis Cluster.
- Circuit breaker autour des services d'infrastructure.
- Mesure du cache hit rate par endpoint.
