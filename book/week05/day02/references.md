# Références

## Documentation principale

- FastAPI — Bigger Applications: `APIRouter`, séparation en plusieurs fichiers, dépendances de routeur.
- FastAPI — Testing: usage de `TestClient` pour tester une application sans lancer de serveur réseau.
- FastAPI — Global Dependencies: dépendances globales et dépendances appliquées à des groupes de routes.
- OpenAI API — Production guidance: request IDs, timeouts, versions de modèles, evals et pratiques de diagnostic.

## Concepts à revoir

- API gateway.
- Middleware HTTP.
- Contrats Pydantic.
- OpenAPI.
- Authentification par clé API.
- Rate limiting.
- Redaction PII.
- Health check vs readiness check.
- Boundary entre API, service applicatif et runtime agentique.

## Lecture orientée AI Engineering

Une API IA doit être conçue comme une frontière de contrôle :

1. elle limite ce qui entre ;
2. elle stabilise ce qui sort ;
3. elle trace chaque exécution ;
4. elle protège les appels coûteux ;
5. elle évite que les détails du modèle deviennent le contrat public.
