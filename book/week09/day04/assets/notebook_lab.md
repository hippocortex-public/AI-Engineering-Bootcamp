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
from examples.week09.knowledge import rrf, ContractError
A = {"chunk_id": "A", "score": 20}
B = {"chunk_id": "B", "score": .9}
C = {"chunk_id": "C", "score": .1}
result = rrf([[A, B, C], [B, A]])
scores = {c["chunk_id"]: c["score"] for c in result}
assert math.isclose(scores["A"], 1/61 + 1/62)
assert scores["A"] == scores["B"]
assert math.isclose(scores["C"], 1/63)
print(result)
```
