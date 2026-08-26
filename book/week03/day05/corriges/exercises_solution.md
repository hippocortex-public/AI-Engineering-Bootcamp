# Corrigé — Exercices — Sharing State

## Exercice 1 — Identifier les couches d'état

1. Brouillon interne d'un agent reviewer : **local state**.
2. Préférence utilisateur "réponds en français" : **long-term memory** si durable, sinon conversation state si temporaire.
3. Résumé validé d'un incident : **shared state**.
4. Historique des trois derniers messages : **conversation state**.
5. Plan d'exécution partagé entre agents : **shared state**.
6. Clé API utilisée par un outil : **secret/configuration**.
7. Statut `needs_clarification` d'un workflow : **conversation state** ou **shared state** selon le périmètre. Dans un workflow multi-agent, c'est généralement du shared state.

## Exercice 2 — Concevoir une entrée d'état

```json
{
  "incident.root_cause": {
    "value": "Timeout base de données sur la requête checkout",
    "version": 1,
    "owner": "backend",
    "visibility": "shared",
    "updated_by": "backend"
  }
}
```

## Exercice 3 — Détecter un conflit

L'écriture doit être refusée car l'agent pense modifier la version `1`, alors que la clé est déjà en version `2`.

Cela signifie qu'un autre agent a modifié la donnée entre la lecture et l'écriture.

Accepter cette écriture écraserait silencieusement une information plus récente.

## Exercice 4 — Snapshot filtré

L'agent `backend` peut voir :

```json
{
  "incident.summary": {
    "value": "erreur 500 sur /checkout",
    "visibility": "shared"
  },
  "incident.status": {
    "value": "investigating",
    "visibility": "public"
  }
}
```

Il ne peut pas voir :

```text
triage.private_notes
```

car la visibilité est `private` et le propriétaire est `triage`.

## Exercice 5 — Handoff minimal

```json
{
  "from": "triage",
  "to": "backend",
  "context": {
    "incident.summary": {
      "value": "erreur 500 sur /checkout",
      "version": 1
    },
    "incident.status": {
      "value": "investigating",
      "version": 1
    },
    "plan.next_action": {
      "value": "inspecter les logs API checkout",
      "version": 1
    }
  }
}
```

## Exercice 6 — Patch atomique

Un patch multi-clés doit être atomique pour éviter un état partiellement modifié.

Si une clé est mise à jour mais qu'une autre échoue, les agents suivants peuvent observer un état incohérent.

La règle correcte est :

```text
valider toutes les écritures, puis appliquer toutes les écritures
```

## Exercice 7 — Trace d'état

```json
{
  "event_id": 1,
  "agent": "coordinator",
  "operation": "write",
  "key": "incident.owner",
  "version": 1,
  "status": "applied"
}
```

## Exercice 8 — Lab

Le fichier `test_shared_state_store.py` montre une implémentation complète des vérifications demandées :

- création d'une clé privée ;
- restriction de lecture ;
- création d'une clé partagée ;
- snapshot filtré ;
- conflit de version ;
- journal d'événements.
