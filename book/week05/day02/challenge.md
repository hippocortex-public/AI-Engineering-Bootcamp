# Challenge — API de support IA production-ready

## Objectif

Étendre le lab pour rendre l'API plus proche d'un environnement production.

## Contexte

Tu disposes d'une API FastAPI exposant :

- `GET /healthz`
- `GET /readyz`
- `POST /v1/chat`
- `GET /v1/sessions/{session_id}`

## Travail demandé

Ajoute une route :

```text
POST /v1/admin/sessions/{session_id}/forget
```

Cette route doit :

1. être protégée par la clé API ;
2. demander un en-tête `X-Human-Approval: approved` ;
3. supprimer la session si elle existe ;
4. retourner une réponse structurée ;
5. retourner `404` si la session n'existe pas ;
6. retourner `403` si l'approbation humaine est absente ;
7. écrire une trace ou un événement d'audit simplifié.

## Contraintes

- Ne pas changer l'arborescence du projet.
- Ne pas supprimer les exports existants.
- Ne pas appeler de service externe.
- Ajouter des tests HTTP.
- Garder une réponse JSON stable.

## Critères d'acceptation

Le challenge est réussi si :

- les tests existants passent toujours ;
- la nouvelle route est visible dans OpenAPI ;
- une session oubliée n'est plus lisible ;
- une suppression sans approbation est refusée ;
- l'API publique reste cumulative.
