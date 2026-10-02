# Lab — FastAPI + Redis pour API IA

## Objectif

Ce lab implémente une petite API FastAPI qui utilise Redis pour :

- limiter le nombre de requêtes par utilisateur ;
- cacher une réponse LLM simulée ;
- stocker un état conversationnel court ;
- exposer un endpoint de santé.

## Arborescence

```text
labs/
├── README.md
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── cache.py
│   ├── rate_limit.py
│   ├── redis_client.py
│   └── schemas.py
└── tests/
    └── test_key_strategy.py
```

## Lancer le lab

Depuis ce dossier :

```bash
docker compose up --build
```

Puis appeler l'API :

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "u_123",
    "conversation_id": "c_456",
    "message": "Explique Redis pour une API IA.",
    "model": "demo-llm",
    "prompt_version": "v1"
  }'
```

Le premier appel doit retourner `source: "llm"`. Un appel identique doit retourner `source: "cache"`.

## Lancer les tests unitaires

```bash
python -m pytest tests
```

Les tests fournis vérifient la stabilité de la stratégie de clé.
