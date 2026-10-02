# Exercices

## Exercice 1 — Concevoir des clés Redis

Pour chacun des cas suivants, proposez une clé Redis conforme à la convention :

```text
{app}:{env}:{domain}:{entity}:{id}
```

Cas :

1. cache d'une réponse LLM pour une classification de ticket ;
2. session conversationnelle d'un utilisateur ;
3. compteur de rate limit par minute ;
4. clé d'idempotence pour une requête HTTP ;
5. verrou court pour empêcher deux workers de traiter le même job.

Livrable attendu : cinq clés et une justification courte.

## Exercice 2 — Construire une clé de cache stable

Écrivez une fonction Python :

```python
def build_cache_key(app: str, env: str, model: str, prompt_version: str, payload: dict) -> str:
    ...
```

Contraintes :

- la clé doit être stable si les champs du dictionnaire sont dans un ordre différent ;
- la clé ne doit pas contenir le prompt complet ;
- la clé doit inclure le modèle et la version du prompt ;
- le hash doit utiliser SHA-256.

Livrable attendu : fonction Python et deux exemples montrant que l'ordre des clés ne change pas le résultat.

## Exercice 3 — Choisir des TTL

Proposez un TTL pour chaque donnée :

| Donnée | TTL à proposer |
|---|---|
| résumé d'un document interne non sensible |
| réponse de chat très contextuelle |
| session conversationnelle courte |
| compteur de rate limit minute |
| clé d'idempotence pour création de job |
| résultat de classification de ticket |

Livrable attendu : tableau complété et justification.

## Exercice 4 — Implémenter un rate limiter simple

Écrivez une fonction asynchrone :

```python
async def allow_request(redis, key: str, limit: int, ttl_seconds: int) -> bool:
    ...
```

Contraintes :

- utiliser `INCR` ;
- poser le TTL uniquement au premier incrément ;
- retourner `True` si la requête est autorisée ;
- retourner `False` si la limite est dépassée.

Livrable attendu : fonction Python + explication du comportement.
