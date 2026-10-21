# Lab exécutable

Cellules autonomes à partir du dépôt; aucune requête réseau.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week08/ops.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from examples.week08.demo import load
from examples.week08.ops import run_security
cases = load("baseline")["security_cases"]
report = run_security(cases)
assert report["count"] == 8 and report["passed"]
assert sum(c["allowed"] for c in report["cases"]) == 2
print(report)
```
