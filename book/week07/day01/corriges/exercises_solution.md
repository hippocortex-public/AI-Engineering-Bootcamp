# Corrigé des exercices

## Exercice 1 — Repérer les responsabilités

Webhook déclenche; HTTP Request transporte; Respond to Webhook répond au demandeur; Engine.ingest valide et écrit dans une transaction. Le transport ne décide pas de la publication.

## Exercice 2 — Comparer les accusés de réception

202 signifie événement durablement accepté. 200 indique qu’un événement identique a déjà été accepté. Le client doit consulter le job pour connaître son état.

## Exercice 3 — Diagnostiquer le réseau

localhost est le conteneur n8n. Utiliser http://backend:8080/events depuis n8n et http://127.0.0.1:8080/events depuis le poste.
