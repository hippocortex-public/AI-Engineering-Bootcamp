# Correction exécutable du lab

Dans Jupyter, démarrer le kernel depuis la racine du dépôt ou depuis son arbre. Ce fragment recherche la racine contenant le module S7. Il utilise le moteur complet, distinct du petit exemple autonome.

```python
from pathlib import Path
import sys
root = next((p for p in [Path.cwd(), *Path.cwd().parents] if (p / "examples/week07/workflow.py").is_file()), None)
if root is None:
    raise RuntimeError("Ouvrir le notebook depuis le dépôt décompressé")
sys.path.insert(0, str(root))
from examples.week07.demo import scenario
result = scenario(3)
assert result == {'duplicate_created': False, 'jobs': {'received': 1}}
print(result)
```

Les assertions constituent la preuve minimale de ce scénario; les tests de `tests/week07` couvrent les branches complémentaires. Le payload canonique contient ticket_id : modifier ce champ avec le même event_id entraîne Conflict. Avec event_id neuf, le job est accepté. Cette différence montre que déduplication technique et politique métier par ticket sont distinctes.
