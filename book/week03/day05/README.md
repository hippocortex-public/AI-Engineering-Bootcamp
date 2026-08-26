# Semaine 3 — Jour 5 — Sharing State

## Position dans le bootcamp

- **Semaine** : 3 — Multi-Agent & MCP
- **Jour** : 5 — Sharing State
- **Thème** : partage d'état entre agents, clients MCP et composants d'orchestration.
- **Pré-requis** :
  - Semaine 2 : conversation state, memory, agent loop.
  - Semaine 3 J1 : architectures multi-agents.
  - Semaine 3 J2 : coordination.
  - Semaine 3 J3 : MCP Server.
  - Semaine 3 J4 : MCP Client.

## Résumé

Un système multi-agent échoue souvent non pas parce que les agents sont faibles, mais parce que leur état est mal partagé.

Cette journée apprend à concevoir un **shared state** contrôlé :

- ce qui est local à un agent ;
- ce qui est partagé entre agents ;
- ce qui est durable ;
- ce qui est temporaire ;
- ce qui doit être versionné ;
- ce qui doit rester privé ;
- ce qui doit être transmis lors d'un handoff ;
- ce qui doit être observable dans les traces.

Le partage d'état n'est pas une mémoire globale libre. C'est un contrat applicatif.

## Objectif de la journée

À la fin de la journée, l'apprenant sait concevoir et implémenter un store d'état partagé pour un workflow multi-agent.

Il sait notamment :

- distinguer **local state**, **shared state**, **conversation state** et **long-term memory** ;
- versionner les écritures pour éviter les conflits ;
- construire des snapshots partiels selon les permissions ;
- transmettre un contexte minimal lors d'un handoff ;
- journaliser les modifications sous forme d'événements ;
- éviter les effets de bord implicites entre agents.

## Livrables

Cette journée contient :

- un chapitre complet ;
- des objectifs pédagogiques ;
- des exercices ;
- des questions d'entretien ;
- un challenge ;
- des corrections ;
- deux diagrammes Mermaid ;
- des assets JSON ;
- un lab Python exécutable ;
- un notebook étudiant ;
- un notebook formateur.

## Lab

Le lab implémente un store d'état partagé en Python standard library :

```text
labs/shared_state_store.py
labs/test_shared_state_store.py
```

Le store supporte :

- lecture/écriture versionnée ;
- compare-and-set ;
- snapshots par agent ;
- état privé, partagé et public ;
- handoff contextuel ;
- patch atomique ;
- journal d'événements ;
- résumé déterministe.

## Commandes de validation

Depuis `book/week03/day05/labs/` :

```bash
python -m py_compile shared_state_store.py test_shared_state_store.py
python test_shared_state_store.py
```

## Message clé

Un bon système multi-agent ne partage pas tout.

Il partage uniquement l'état nécessaire, au bon niveau de granularité, avec des règles de version, d'accès et d'observabilité.
