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
from examples.week08.ops import telemetry
runs = load("candidate")["runs"]
signals = telemetry(runs)
assert signals["metrics"]["requests_by_status"] == {"ok": 35, "timeout": 1, "error": 0}
allowed = {"trace_id", "span_id", "parent_span_id", "version", "status", "duration_ms"}
assert all(set(row) == allowed for row in signals["logs"])
print(signals["metrics"])
```
