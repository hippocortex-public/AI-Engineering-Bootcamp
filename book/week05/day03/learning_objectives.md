# Objectifs pédagogiques

## Objectifs principaux

À la fin de ce jour, l'apprenant doit être capable de :

1. expliquer le rôle de Redis dans une architecture IA de production ;
2. distinguer cache, état court terme, verrou, idempotence et rate limiting ;
3. concevoir une stratégie de clés Redis lisible et maintenable ;
4. implémenter un cache LLM en stratégie cache-aside ;
5. stocker un état conversationnel court avec expiration ;
6. construire un rate limiter simple et atomique ;
7. intégrer Redis dans une API FastAPI ;
8. identifier les limites de Redis pour les données durables ;
9. appliquer les bonnes pratiques de sécurité autour des prompts, réponses et données utilisateur ;
10. produire un lab exécutable et testable.

## Compétences AI Engineering ciblées

- Architecture de systèmes IA à latence contrôlée.
- Réduction des coûts d'appels LLM.
- Gestion d'état temporaire pour agents et assistants.
- Protection d'une API contre les abus et les pics de charge.
- Séparation entre stockage volatil et stockage durable.
- Design de clés et TTL en environnement multi-utilisateur.

## Pré-requis

L'apprenant doit avoir compris :

- les principes d'une API FastAPI ;
- les appels LLM simulés ou réels ;
- les notions de requête, réponse, latence et coût ;
- les bases de Python asynchrone ;
- les risques liés à la persistance de données sensibles.

## Critères de réussite

La journée est réussie si l'apprenant peut :

- expliquer pourquoi un cache LLM peut être dangereux s'il ignore l'utilisateur ou le contexte ;
- coder une fonction `get_or_set` avec TTL ;
- justifier un TTL différent pour une réponse LLM, une session et un compteur de rate limit ;
- définir une convention de clés Redis ;
- exécuter le lab localement avec Docker Compose.
