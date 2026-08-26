# Lab — Memory Layer

## Objectif

Implémenter et tester une couche mémoire pour le mini-framework d'agents.

## Fichiers

```text
memory_layer_lab.py
test_memory_layer.py
```

Le module principal du framework est :

```text
mini_framework/memory.py
```

## Exécution

Depuis ce dossier :

```bash
python memory_layer_lab.py
python test_memory_layer.py
```

## Ce que le lab démontre

- création de records mémoire ;
- isolation par namespace ;
- filtrage par visibilité ;
- expiration TTL ;
- redaction PII ;
- scoring déterministe ;
- promotion d'événements ;
- oubli namespace ;
- snapshot/restore ;
- audit log.
