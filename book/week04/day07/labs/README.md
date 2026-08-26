# Lab — Intégration du mini-framework

## Objectif

Assembler les composants d'un mini-framework d'agents dans une exécution complète.

## Fichiers

```text
integration_lab.py
test_integration.py
```

Le code principal réutilisable est dans :

```text
mini_framework/integration.py
```

## Exécution

Depuis la racine du livrable :

```bash
python -m py_compile mini_framework/integration.py book/week04/day07/labs/integration_lab.py book/week04/day07/labs/test_integration.py
python book/week04/day07/labs/test_integration.py
```

## Ce que le lab démontre

- Déclaration d'agents
- Enregistrement d'outils
- Validation d'arguments
- Outils sensibles
- Approbation humaine
- Mémoire utilisateur
- Workflow déterministe
- Trace d'exécution
- Résultat JSON
- Tests de sécurité et d'intégration
