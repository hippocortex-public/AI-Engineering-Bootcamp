# Lab — Abstraction Agent

## Objectif

Implémenter et tester une abstraction `Agent` indépendante d’un fournisseur LLM.

## Fichiers

- `agent_abstraction.py` : implémentation pédagogique.
- `test_agent_abstraction.py` : tests unitaires.

## Exécution

Depuis ce dossier :

```bash
python agent_abstraction.py
python test_agent_abstraction.py
```

## Points observables

Le lab montre :

- une classe `Agent` ;
- un `RunContext` ;
- un `AgentResult` ;
- un `ModelClient` abstrait ;
- un faux modèle déterministe ;
- des guardrails simples ;
- des traces ;
- une sortie JSON sérialisable.

## Pourquoi aucun appel API réel ?

Cette journée teste l’abstraction logicielle, pas la qualité d’un modèle. Les appels réels seront branchés plus tard derrière l’interface `ModelClient`.
