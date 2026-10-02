# Corrigé — Questions d'entretien

## Réponse 1

Redis est utile dans une API IA de production car il fournit une couche mémoire rapide pour réduire la latence, diminuer les appels LLM redondants, stocker un état conversationnel court et protéger l'API avec du rate limiting.

## Réponse 2

Redis stocke des données volatiles, temporaires ou recalculables. PostgreSQL stocke les données durables et transactionnelles. Dans cette architecture, Redis sert à accélérer et protéger ; PostgreSQL sert de source de vérité.

## Réponse 3

La version du prompt système doit être incluse car une modification du prompt peut changer complètement la réponse attendue. Sans version, l'API pourrait retourner une ancienne réponse devenue incorrecte.

## Réponse 4

Un cache LLM mal conçu peut retourner une réponse d'un autre contexte, exposer indirectement des données sensibles, masquer une mise à jour de prompt, ignorer des permissions ou produire des incohérences entre utilisateurs.

## Réponse 5

Le TTL d'une session conversationnelle dépend de l'expérience utilisateur, de la sensibilité des données et du coût de reconstruction de l'état. Pour un assistant standard, 30 à 60 minutes est souvent un bon point de départ.

## Réponse 6

Un rate limiter simple utilise une clé par utilisateur et par fenêtre. On incrémente la clé avec `INCR`, on pose un TTL au premier incrément et on refuse lorsque le compteur dépasse la limite.

## Réponse 7

Le comportement dépend de l'usage. Pour un cache, l'API peut bypasser Redis. Pour l'idempotence ou le rate limiting d'une API publique, un mode strict peut être préférable afin d'éviter les abus ou les doublons.

## Réponse 8

Redis ne doit pas contenir toute la mémoire d'un agent car cette mémoire peut être durable, volumineuse, sensible et nécessiter des requêtes complexes. Redis convient surtout à l'état court et opérationnel.

## Réponse 9

Il faut observer le cache hit rate, le cache miss rate, la latence Redis, les erreurs Redis, le nombre de requêtes bloquées par rate limit et les évictions de clés.

## Réponse 10

L'idempotence garantit qu'une même requête logique ne produit pas deux fois le même effet. Pour un appel IA coûteux, une clé d'idempotence évite de lancer deux générations ou deux jobs lorsqu'un client réessaie après un timeout.
