# Stratégie de clés Redis

## Convention

```text
{app}:{env}:{domain}:{entity}:{id}
```

## Exemples

```text
ai-api:dev:cache:llm:demo-llm:v1:hash:0f4c2a9d11e8b000
ai-api:dev:session:user:u_123:conv:c_456
ai-api:dev:ratelimit:user:u_123:minute
ai-api:dev:idempotency:req:req_789
```

## Règles

- Ne jamais mettre un secret dans une clé.
- Ne jamais mettre un prompt complet dans une clé.
- Utiliser un hash stable pour les payloads.
- Inclure la version du prompt.
- Préfixer par application et environnement.
- Choisir un TTL explicite.
