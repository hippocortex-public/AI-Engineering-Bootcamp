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
result = scenario(6)
assert result == {'status': 'published', 'publication_count': 1}
print(result)
```

Les assertions constituent la preuve minimale de ce scénario; les tests de `tests/week07` couvrent les branches complémentaires. Après process, conserver proposal_hash. Appeler decide deux fois avec approve et reviewer-demo; les deux appels retournent published. Compter publications :1. Appeler reject avec le même hash :Conflict. Le test test_approval_idempotent est la correction exécutable.
