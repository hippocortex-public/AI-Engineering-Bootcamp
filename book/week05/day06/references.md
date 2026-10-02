# Références — Sécurité IA

## Sources primaires consultées le 1er octobre 2026

- OWASP GenAI, Prompt Injection, page de la nomenclature 2025 :
  https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- OWASP GenAI, Excessive Agency, page de la nomenclature 2025 :
  https://genai.owasp.org/llmrisk/llm062025-excessive-agency/
- FastAPI, outils de sécurité et `APIKeyHeader` :
  https://fastapi.tiangolo.com/reference/security/
- Python, `hmac.compare_digest` : https://docs.python.org/3/library/hmac.html
- Pydantic, modèles et gestion des champs supplémentaires :
  https://docs.pydantic.dev/latest/concepts/models/

Les numéros OWASP cités identifient les pages 2025 consultées ; ils ne servent pas
à affirmer qu'il s'agit de la seule nomenclature disponible. Le cours se concentre
sur les principes plutôt que sur la mémorisation des numéros.

## Documentation pour les extensions

- PostgreSQL, Row Security : https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- Redis, scripting : https://redis.io/docs/latest/develop/programmability/eval-intro/
- OpenID Connect Core : https://openid.net/specs/openid-connect-core-1_0.html

## Liens internes

- S5 J2 : validation des endpoints et dépendances FastAPI.
- S5 J3 : cache Redis, TTL et politiques de clé.
- S5 J4 : persistance, transactions et requêtes paramétrées.
- S5 J5 : métriques, corrélation et diagnostic.
- S5 J7 : déploiement, prévu par la roadmap.
