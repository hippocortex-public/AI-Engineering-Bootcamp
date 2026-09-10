# Lab — API FastAPI

## Objectif

Construire et tester une API FastAPI pour un assistant IA de support.

## Commandes

Depuis la racine du dépôt :

```bash
python book/week05/day02/labs/api_fastapi_lab.py
python book/week05/day02/labs/test_api_fastapi.py
```

## Points couverts

- création d'application FastAPI ;
- routeur `/v1` ;
- authentification par `X-API-Key` ;
- request ID ;
- schémas Pydantic stricts ;
- rate limiting pédagogique ;
- redaction PII ;
- session transcript ;
- tests avec `TestClient`.

## Note

Le service d'IA est déterministe afin de rendre le lab exécutable sans clé API externe.
