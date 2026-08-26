# Lab — Conversation State

## Objectif

Construire un mini-agent de support client qui maintient un état conversationnel entre plusieurs tours.

Le lab est volontairement déterministe.

Aucun appel à une API externe n’est nécessaire.

## Fichiers

```text
conversation_state_agent.py
test_conversation_state_agent.py
```

## Exécution

Depuis ce dossier :

```bash
python conversation_state_agent.py
python test_conversation_state_agent.py
```

## Ce que le lab démontre

- Initialisation d’un état par session.
- Détection d’intention.
- Extraction de slots simples.
- Conservation de l’intention entre les tours.
- Calcul des champs manquants.
- Génération de questions ciblées.
- Protection contre les actions prématurées.
- Sérialisation et restauration JSON.
- Isolation entre deux sessions.

## Limite volontaire

L’extraction est faite avec des règles simples.

Dans un agent réel, cette étape peut être remplacée par un modèle produisant un Structured Output validé.

Le reste de l’architecture reste identique :

```text
message
→ extraction
→ update state
→ missing fields
→ action policy
→ response
```
