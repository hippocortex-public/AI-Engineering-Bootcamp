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
result = scenario(7)
assert result == {'statuses': {'expired': 1, 'published': 1, 'rejected': 1}, 'publication_count': 1}
print(result)
```

Les assertions constituent la preuve minimale de ce scénario; les tests de `tests/week07` couvrent les branches complémentaires. Exécuter demo 7, la suite unittest, puis les trois workflows n8n si Docker est disponible. Le scénario Python doit produire published:1, rejected:1, expired:1 et une publication. L’ADR expose le contexte, la décision, l’alternative « logique dans n8n », les conséquences et les limites. Une validation n8n non réalisée doit rester marquée non vérifiée.
