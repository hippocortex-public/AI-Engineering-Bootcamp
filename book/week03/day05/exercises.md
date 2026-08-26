# Exercices — Sharing State

## Exercice 1 — Identifier les couches d'état

Classez chaque élément dans une couche :

1. brouillon interne d'un agent reviewer ;
2. préférence utilisateur "réponds en français" ;
3. résumé validé d'un incident ;
4. historique des trois derniers messages ;
5. plan d'exécution partagé entre agents ;
6. clé API utilisée par un outil ;
7. statut `needs_clarification` d'un workflow.

Catégories possibles :

- local state ;
- conversation state ;
- shared state ;
- long-term memory ;
- secret/configuration.

## Exercice 2 — Concevoir une entrée d'état

Proposez une structure JSON pour représenter la clé suivante :

```text
incident.root_cause
```

Contraintes :

- version ;
- propriétaire ;
- visibilité ;
- agent ayant effectué la dernière modification ;
- valeur.

## Exercice 3 — Détecter un conflit

Soit l'état :

```json
{
  "plan.next_step": {
    "value": "inspect logs",
    "version": 2
  }
}
```

Un agent tente d'écrire :

```json
{
  "key": "plan.next_step",
  "value": "restart service",
  "expected_version": 1
}
```

Expliquez pourquoi l'écriture doit être refusée.

## Exercice 4 — Snapshot filtré

L'état contient :

```json
{
  "triage.private_notes": {
    "value": "hypothèse non vérifiée",
    "visibility": "private",
    "owner": "triage"
  },
  "incident.summary": {
    "value": "erreur 500 sur /checkout",
    "visibility": "shared",
    "owner": "triage"
  },
  "incident.status": {
    "value": "investigating",
    "visibility": "public",
    "owner": "coordinator"
  }
}
```

Quelles clés l'agent `backend` peut-il voir ?

## Exercice 5 — Handoff minimal

Un agent `triage` transmet la tâche à `backend`.

Concevez un handoff contenant uniquement :

- le résumé de l'incident ;
- le statut ;
- la prochaine action demandée.

## Exercice 6 — Patch atomique

Expliquez pourquoi un patch multi-clés doit être appliqué entièrement ou refusé entièrement.

## Exercice 7 — Trace d'état

Définissez un événement JSON minimal pour une écriture réussie sur la clé :

```text
incident.owner
```

## Exercice 8 — Lab

Dans le fichier `shared_state_store.py` :

1. créez une clé privée ;
2. vérifiez qu'un autre agent ne peut pas la lire ;
3. créez une clé partagée ;
4. construisez un snapshot pour un autre agent ;
5. déclenchez un conflit de version ;
6. affichez le journal d'événements.
