# Lab exécutable

Les cellules lisent les fixtures distribuées. Elles ne contactent aucun modèle.

```python
from pathlib import Path
import sys
import json
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "book/week08/day01/labs/evaluation_lab").is_dir()), None)
assert root is not None, "Ouvrir le notebook dans le dépôt"
day = root / "book/week08/day01"
sys.path.insert(0, str(day / "labs"))
from evaluation_lab.core import read_rows, evaluate, compare
dataset = read_rows(day / "assets/dataset.jsonl")
baseline = evaluate(dataset, read_rows(day / "assets/baseline.jsonl"))
candidate = evaluate(dataset, read_rows(day / "assets/candidate.jsonl"))
print(json.dumps({"baseline": baseline["rate"], "candidate": candidate["rate"], "comparison": compare(baseline, candidate)}, indent=2))
assert baseline["accepted"] and not candidate["accepted"]
```

Inspecter la distribution des réussites et les effectifs.

```python
for name, report in (("baseline", baseline), ("candidate", candidate)):
    print(name, report["segments"], "coverage:", report["coverage"])
assert compare(baseline, candidate)["regressions"] == ["c09"]
```
