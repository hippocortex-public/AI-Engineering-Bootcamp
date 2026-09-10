# Objectifs pédagogiques

À la fin de cette journée, l'apprenant doit être capable de :

1. expliquer le rôle de FastAPI dans une plateforme IA de production ;
2. concevoir une frontière claire entre transport HTTP, service applicatif et runtime agentique ;
3. créer des contrats Pydantic stricts pour les entrées et sorties ;
4. structurer une application avec `FastAPI`, `APIRouter`, dépendances et middleware ;
5. exposer des endpoints `/healthz`, `/readyz`, `/v1/chat` et `/v1/sessions/{session_id}` ;
6. appliquer une authentification simple par `X-API-Key` ;
7. propager un `X-Request-ID` pour faciliter le debug production ;
8. stabiliser les erreurs HTTP dans une enveloppe JSON exploitable ;
9. tester une API FastAPI avec `TestClient` sans lancer de serveur réseau ;
10. préserver une API publique Python cumulative dans `ai_platform/__init__.py`.

## Compétences AI Engineering

- API design pour workloads LLM.
- Validation avant appel modèle.
- Isolation de session.
- Rate limiting applicatif.
- Redaction PII.
- Observabilité minimale par request ID.
- Tests d'intégration HTTP.
