# Lab — Simulation d’une architecture multi-agents

## Objectif

Implémenter une architecture multi-agents déterministe et testable.

Le lab couvre :

- agents spécialisés ;
- router ;
- manager-worker ;
- handoff ;
- reviewer ;
- exécution parallèle ;
- traces ;
- sérialisation JSON ;
- extension avec un nouvel agent.

## Exécution

Depuis ce dossier :

```bash
python multi_agent_architecture.py
python test_multi_agent_architecture.py
```

## Travail demandé

1. Lire le code.
2. Exécuter les tests.
3. Ajouter un agent `security`.
4. Ajouter un test de routage vers `security`.
5. Expliquer pourquoi le reviewer ne doit pas résoudre la demande métier.
