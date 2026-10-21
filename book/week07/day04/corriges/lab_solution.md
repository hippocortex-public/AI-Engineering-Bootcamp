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
result = scenario(4)
assert result == {'calls': 2, 'status': 'awaiting_review'}
print(result)
```

Les assertions constituent la preuve minimale de ce scénario; les tests de `tests/week07` couvrent les branches complémentaires. Le test test_retry_backoff_and_dead_letter montre les trois échecs avec horloge injectée. Après replay et tick, état awaiting_review. Interroger audit pour event_id : la séquence contient retry, retry, dead_letter, replayed, draft_created. Aucun effet de publication ne doit exister.
