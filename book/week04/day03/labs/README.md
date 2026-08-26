# Lab — Tool Registry

## Objectif

Construire et tester le registre d’outils du mini-framework.

## Fichiers

```text
mini_framework/tool_registry.py
book/week04/day03/labs/tool_registry_lab.py
book/week04/day03/labs/test_tool_registry.py
```

## Exécution

Depuis la racine du projet :

```bash
python book/week04/day03/labs/tool_registry_lab.py
python book/week04/day03/labs/test_tool_registry.py
```

## Contraintes

- Aucune dépendance externe.
- Aucun appel réseau.
- Aucune clé API.
- Validation et politique avant exécution.
- Résultats sérialisables en JSON.

## Expérimentations suggérées

- Ajouter un outil `calculate_discount`.
- Ajouter un scope `pricing:read`.
- Créer un outil sensible nécessitant approbation.
- Observer la différence entre `blocked` et `failed`.
