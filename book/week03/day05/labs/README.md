# Lab — Shared State Store

## Objectif

Implémenter un store d'état partagé pour un système multi-agent.

Le lab montre comment :

- stocker des clés versionnées ;
- filtrer les lectures selon la visibilité ;
- détecter les conflits d'écriture ;
- appliquer un patch atomique ;
- produire un handoff minimal ;
- journaliser les changements.

## Fichiers

```text
shared_state_store.py
test_shared_state_store.py
```

## Exécution

Depuis ce dossier :

```bash
python -m py_compile shared_state_store.py test_shared_state_store.py
python test_shared_state_store.py
```

## Contraintes

Le lab utilise uniquement la Python standard library.

Aucune clé API n'est nécessaire.
