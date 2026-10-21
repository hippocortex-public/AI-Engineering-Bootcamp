# Lab exécutable

Cellules autonomes à partir du dépôt; aucune requête réseau.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week08/ops.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from examples.week08.ops import percentile, benchmark, EvidenceError
from examples.week08.demo import load
assert percentile([100, 200, 300, 1000], .5) == 200
assert percentile([100, 200, 300, 1000], .95) == 1000
data = load("candidate")
ids = [c["id"] for c in data["evaluation"]["cases"]]
result = benchmark(data["runs"], ids)
assert result["count"] == 36 and result["p95_ms"] == 461
assert result["max_ms"] == 2200
print(result)
```
