# Lab exécutable

Cellules autonomes à partir du dépôt; aucune requête réseau.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week08/ops.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from decimal import Decimal
from examples.week08.demo import load
from examples.week08.ops import cost_report, Budget
data = load("baseline")
passed = {c["id"] for c in data["evaluation"]["cases"] if c["passed"]}
report = cost_report(data["runs"], data["prices"], passed)
assert Decimal(report["total_usd"]) == Decimal("0.06084")
assert report["successful_attempts"] == 30
assert Decimal(report["usd_per_success"]) == Decimal("0.002028")
print(report)
```
