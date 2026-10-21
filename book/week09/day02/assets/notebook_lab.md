# Lab exécutable

Les cellules s’exécutent hors ligne depuis l’arbre du dépôt.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week09/knowledge.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
import math
from examples.week09.knowledge import HashEmbedding, cosine, ContractError
encoder = HashEmbedding(128)
a = encoder.encode("Kafka paiement")
b = encoder.encode("paiement Kafka")
assert a == b and math.isclose(cosine(a, b), 1.0)
assert math.isclose(cosine([1, 0], [1, 1]), 1 / math.sqrt(2))
assert cosine([0, 0], [1, 1]) == 0
print(encoder.fingerprint)
```
