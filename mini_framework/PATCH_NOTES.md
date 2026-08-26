# Correctif — `mini_framework/__init__.py` cumulatif

## Problème corrigé

Les livraisons successives de la semaine 4 contenaient chacune un fichier
`mini_framework/__init__.py` propre au jour généré. En extraction séquentielle,
le dernier fichier écrasait les exports précédents.

Conséquence : les modules déjà présents dans `mini_framework/` restaient
physiquement dans le dépôt, mais l'API publique du package ne les exposait plus.

## Correction appliquée

Ce correctif fournit un fichier `mini_framework/__init__.py` cumulatif couvrant
les jours 1 à 7 de la semaine 4 :

- J1 — `architecture`
- J2 — `agent`
- J3 — `tool_registry`
- J4 — `memory`
- J5 — `workflow`
- J6 — `observability`
- J7 — `integration`

Le fichier importe aussi les modules eux-mêmes, afin que les imports suivants
restent stables :

```python
from mini_framework import ToolRegistry
from mini_framework import MemoryStore
from mini_framework import WorkflowEngine
from mini_framework import MiniAgentFramework
from mini_framework import tool_registry, memory, workflow, integration
```

## Gestion des collisions de noms

Le jour 7 définit des classes d'intégration portant les mêmes noms que des
classes spécialisées construites les jours précédents, par exemple :

- `ToolRegistry`
- `ToolResult`
- `MemoryStore`
- `WorkflowStep`
- `WorkflowDefinition`
- `TraceEvent`

La règle retenue est :

1. les noms canoniques pointent vers les modules spécialisés ;
2. les noms d'intégration restent disponibles via des alias explicites.

Exemples :

```python
from mini_framework import ToolRegistry
from mini_framework import IntegrationToolRegistry
```

## Test ajouté

Le fichier suivant vérifie que l'API publique est cumulative :

```text
tests/test_mini_framework_public_api.py
```

Commande de validation :

```bash
python -S tests/test_mini_framework_public_api.py
```

## Propositions d'amélioration

Sans modifier les spécifications figées, la génération des prochains jours
devrait appliquer une règle interne :

> Quand un fichier racine partagé existe déjà dans un livrable précédent,
> le nouveau livrable doit le régénérer en mode cumulatif, jamais en mode
> remplacement isolé.

Cela concerne particulièrement :

- `mini_framework/__init__.py`
- `ai_platform/__init__.py`
- futurs index de package
- fichiers de manifeste globaux éventuels
