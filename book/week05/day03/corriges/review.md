# Review — Semaine 5 Jour 3

## Checklist pédagogique

- L'apprenant sait expliquer le rôle de Redis dans une plateforme IA.
- L'apprenant distingue cache, session, rate limit et idempotence.
- L'apprenant sait écrire une clé Redis maintenable.
- L'apprenant sait choisir un TTL selon la donnée.
- L'apprenant sait implémenter un cache-aside simple.
- L'apprenant sait intégrer Redis dans FastAPI.
- L'apprenant comprend que Redis n'est pas une base durable.
- L'apprenant identifie les risques de sécurité liés au stockage de prompts.

## Points d'attention formateur

Insister sur trois idées :

1. Redis accélère, mais ne décide pas.
2. Le TTL est une décision produit et architecture.
3. Une clé de cache LLM doit représenter tout ce qui rend la réponse correcte.

## Erreurs fréquentes

| Erreur | Correction attendue |
|---|---|
| Mettre le prompt complet dans la clé | Utiliser un hash stable |
| Oublier la version du prompt | Ajouter `prompt_version` |
| Stocker une session sans expiration | Ajouter un TTL |
| Utiliser Redis comme base principale | Réserver PostgreSQL aux données durables |
| Cacher une réponse personnalisée sans `user_id` ou contexte | Inclure le contexte pertinent dans la clé |
| Ignorer la panne Redis | Définir un mode dégradé par usage |

## Questions de validation rapide

- Que se passe-t-il si le prompt système change mais pas la clé Redis ?
- Pourquoi un cache hit rate très bas peut-il être un problème de design de clé ?
- Quel usage Redis peut être bypassé le plus facilement en cas de panne ?
- Pourquoi un rate limiter indisponible peut-il être critique ?
- Quelle donnée doit être stockée dans PostgreSQL plutôt que Redis ?

## Décision de passage au jour 4

L'apprenant peut passer au jour 4 lorsqu'il comprend que PostgreSQL sera introduit comme source de vérité durable, en complément de Redis.
