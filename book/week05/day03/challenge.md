# Challenge — Couche Redis pour API IA

## Contexte

Vous travaillez sur une API FastAPI qui expose un endpoint `/chat`. Chaque requête contient :

- un `user_id` ;
- un `conversation_id` ;
- un message utilisateur ;
- un nom de modèle ;
- une version de prompt système.

L'appel au modèle est coûteux. L'API doit être protégée contre les abus et doit conserver un historique conversationnel court.

## Objectif

Concevoir et implémenter une couche Redis qui fournit :

1. un cache de réponse LLM ;
2. une session conversationnelle courte ;
3. un rate limiter par utilisateur ;
4. une stratégie de clés claire ;
5. une politique de TTL ;
6. un comportement dégradé si Redis est indisponible.

## Contraintes

- Le cache doit utiliser SHA-256.
- La session doit expirer.
- Le rate limiter doit utiliser `INCR` + `EXPIRE`.
- Les clés doivent être préfixées par application et environnement.
- Les données sensibles ne doivent pas apparaître en clair dans les clés.
- La solution doit être compatible avec FastAPI.
- Le code doit être compréhensible par un AI Backend Engineer junior.

## Livrables attendus

1. diagramme Mermaid de l'architecture ;
2. table des clés Redis ;
3. code Python de la couche cache ;
4. code Python du rate limiter ;
5. exemple d'intégration dans un endpoint FastAPI ;
6. explication des choix de TTL ;
7. limites de la solution.

## Barème indicatif

| Critère | Points |
|---|---:|
| Stratégie de clés | 20 |
| Cache LLM stable | 20 |
| Session courte avec TTL | 15 |
| Rate limiter correct | 15 |
| Intégration FastAPI | 15 |
| Résilience et sécurité | 10 |
| Clarté de l'explication | 5 |
