# Contrat HTTP du lab

Content-Type : application/json. Les endpoints protégés exigent `Authorization: Bearer <token>`. Le token service ne permet pas de décider; le token revue ne permet pas d’ingérer.

| Méthode et chemin | Rôle | Résultat nominal |
|---|---|---|
| GET /health | Public local | 200, statut ok |
| POST /events | Service | 202 nouveau; 200 doublon |
| POST /tick | Service | 200, jobs traités |
| GET /jobs/{event_id} | Service | 200, état et proposition |
| GET /metrics | Service | 200, compteurs JSON |
| POST /jobs/{event_id}/decision | Revue | 200, résultat terminal |
| POST /jobs/{event_id}/replay | Revue | 200, dead letter remise en received |

POST /events exige exactement event_id, schema_version, type, ticket_id, text. Version : entier 1; type : support.requested. Identifiants : lettres ASCII, chiffres, tiret et underscore, longueur 1 à 100. Text : non vide, limité à 4000 caractères. Corps HTTP : limité à 16000 octets.

POST /decision exige exactement decision et proposal_hash. Decision vaut approve ou reject. Le hash vient de GET /jobs; l’acteur est dérivé du rôle côté serveur. POST /tick et /replay peuvent recevoir `{}`.

| Erreur | Status |
|---|---|
| Token absent, invalide ou mauvais rôle | 401 |
| Contrat ou JSON invalide | 400 |
| Job ou chemin inconnu | 404 |
| Identifiant réutilisé, hash obsolète, expiration ou décision contradictoire | 409 |
| Taille absente, nulle ou trop grande | 413 |

/metrics est un comptage JSON, pas un format Prometheus. Le moteur ne traite automatiquement que received/retry éligibles. Il conserve les données sans purge métier; utiliser des fixtures fictives. L’audit local est modifiable par le propriétaire du stockage.
