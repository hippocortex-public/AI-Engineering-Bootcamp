# Corrigé — Exercices

## Exercice 1 — Concevoir des clés Redis

Propositions possibles :

| Cas | Clé proposée | Justification |
|---|---|---|
| Cache classification ticket | `ai-api:prod:cache:ticket-classification:v1:hash:9d2c4a` | inclut domaine, version et hash plutôt que contenu brut |
| Session conversationnelle | `ai-api:prod:session:user:u_123:conv:c_456` | rattache l'état court à un utilisateur et une conversation |
| Rate limit minute | `ai-api:prod:ratelimit:user:u_123:minute:202609111140` | fenêtre temporelle explicite |
| Idempotence HTTP | `ai-api:prod:idempotency:req:req_789` | empêche de retraiter la même requête |
| Verrou worker | `ai-api:prod:lock:job:j_456` | verrou court par job |

L'idée essentielle est d'éviter les clés anonymes comme `cache:123`, impossibles à exploiter en production.

## Exercice 2 — Construire une clé de cache stable

```python
import hashlib
import json

def build_cache_key(app: str, env: str, model: str, prompt_version: str, payload: dict) -> str:
    canonical_payload = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()
    return f"{app}:{env}:cache:llm:{model}:{prompt_version}:hash:{digest[:16]}"
```

Démonstration :

```python
payload_a = {"text": "Bonjour", "task": "classify"}
payload_b = {"task": "classify", "text": "Bonjour"}

key_a = build_cache_key("ai-api", "dev", "gpt-x", "prompt-v1", payload_a)
key_b = build_cache_key("ai-api", "dev", "gpt-x", "prompt-v1", payload_b)

assert key_a == key_b
print(key_a)
```

L'option `sort_keys=True` rend le JSON stable. Le prompt complet n'apparaît pas dans la clé.

## Exercice 3 — Choisir des TTL

| Donnée | TTL proposé | Justification |
|---|---:|---|
| Résumé d'un document interne non sensible | 24 h | contenu probablement stable sur une journée |
| Réponse de chat très contextuelle | 5 à 15 min | dépend du contexte immédiat |
| Session conversationnelle courte | 1 h | équilibre entre continuité UX et minimisation des données |
| Compteur de rate limit minute | 60 s | correspond à la fenêtre de contrôle |
| Clé d'idempotence pour création de job | 24 h | évite les doublons liés aux retries client |
| Résultat de classification de ticket | 7 jours | classification souvent stable si le modèle et le prompt ne changent pas |

Le bon TTL dépend toujours du risque métier, du coût de recalcul et de la sensibilité des données.

## Exercice 4 — Rate limiter simple

```python
async def allow_request(redis, key: str, limit: int, ttl_seconds: int) -> bool:
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, ttl_seconds)
    return count <= limit
```

Comportement :

- première requête : compteur à 1, TTL posé ;
- requêtes suivantes : compteur incrémenté ;
- tant que `count <= limit`, la requête passe ;
- lorsque `count > limit`, la requête est bloquée ;
- à expiration du TTL, la fenêtre repart à zéro.

Limite : cette version utilise une fenêtre fixe. Deux rafales proches de la frontière de fenêtre peuvent laisser passer plus de requêtes qu'une fenêtre glissante stricte.
