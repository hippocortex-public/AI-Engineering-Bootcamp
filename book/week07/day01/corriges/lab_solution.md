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
result = scenario(1)
assert result == {'accepted': True, 'status': 'received'}
print(result)
```

Les assertions constituent la preuve minimale de ce scénario; les tests de `tests/week07` couvrent les branches complémentaires. Exécuter le scénario curl décrit dans docs/week07/QUICKSTART.md. Attendre 202 puis 200. GET /metrics doit contenir un seul job pour cet event_id. Dans n8n, deux exécutions peuvent exister : ce nombre ne prouve pas deux jobs. Si Docker est indisponible, reproduire les deux POST directement sur le backend et marquer la vérification n8n comme non effectuée.
