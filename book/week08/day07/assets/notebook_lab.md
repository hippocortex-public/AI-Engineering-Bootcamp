# Lab exécutable

Cellules autonomes à partir du dépôt; aucune requête réseau.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week08/ops.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from examples.week08.demo import scenario
baseline = scenario(7, "baseline")
candidate = scenario(7, "candidate")
assert baseline["accepted"]
assert not candidate["accepted"]
assert candidate["failed_checks"] == ["quality"]
assert candidate["quality"]["rate"] > baseline["quality"]["rate"]
print({"baseline": baseline["checks"], "candidate": candidate["checks"]})
```
