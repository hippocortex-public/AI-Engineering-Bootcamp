# Challenge — Shared State Coordinator

## Contexte

Vous construisez un assistant multi-agent pour traiter des incidents de production.

Le workflow contient :

- un agent `triage` ;
- un agent `backend` ;
- un agent `security` ;
- un agent `reviewer` ;
- un coordinateur.

## Objectif

Étendre le lab pour construire un `SharedStateCoordinator`.

Le coordinateur doit :

1. recevoir un objectif utilisateur ;
2. initialiser un état partagé ;
3. demander un patch à `triage` ;
4. demander un patch à `backend` ;
5. demander un patch à `security` si l'incident semble sensible ;
6. transmettre un handoff minimal au `reviewer` ;
7. produire une synthèse finale ;
8. exposer le journal d'événements.

## Contraintes

Le système doit respecter ces règles :

- aucun agent ne peut lire une clé `private` dont il n'est pas propriétaire ;
- chaque écriture doit être versionnée ;
- un patch multi-clés doit être atomique ;
- le reviewer ne doit recevoir que les clés nécessaires ;
- le système doit détecter les conflits ;
- le journal d'événements doit être exploitable ;
- aucune mémoire long terme ne doit être utilisée pour stocker l'état temporaire de l'incident.

## Sortie attendue

Le coordinateur doit produire un dictionnaire :

```json
{
  "status": "completed",
  "summary": "...",
  "handoff": {...},
  "state": {...},
  "events": [...]
}
```

## Bonus

Ajoutez une méthode :

```python
export_as_mcp_resource(uri: str) -> dict
```

Elle doit exposer uniquement les clés publiques ou explicitement partagées.
