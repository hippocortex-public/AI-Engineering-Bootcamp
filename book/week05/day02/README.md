# Semaine 5 — Jour 2 : API FastAPI

## Position dans le bootcamp

La semaine 5 transforme les briques agentiques en **système IA de production**.  
Le jour 1 a posé l'architecture production. Le jour 2 expose cette architecture derrière une API HTTP maintenable.

Roadmap : Semaine 5 — Production AI Systems, Jour 2 — API FastAPI.

## Objectif du jour

Construire une API FastAPI pour un assistant IA de support, avec contrats d'entrée/sortie, validation, authentification, health checks, readiness, rate limiting pédagogique, traçabilité de requête et tests automatisés.

## Résultat attendu

À la fin de la journée, l'apprenant sait :

- séparer la couche HTTP de la logique agentique ;
- définir des schémas Pydantic stricts pour les requêtes et réponses ;
- exposer des routes de production avec `APIRouter` ;
- ajouter authentification par clé API, request ID et erreurs stables ;
- tester l'API avec `TestClient` ;
- maintenir un package `ai_platform` cumulatif.

## Lab

```bash
python book/week05/day02/labs/api_fastapi_lab.py
python book/week05/day02/labs/test_api_fastapi.py
```

## Package enrichi

```text
ai_platform/
├── __init__.py
├── architecture.py
└── api.py
```

Le `__init__.py` conserve les exports du jour 1 et ajoute ceux du jour 2.
