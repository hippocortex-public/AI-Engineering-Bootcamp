# Lab exécutable

NumPy et scikit-learn sont requis; aucune requête réseau dans les cellules.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week10/nlp.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from examples.week10.nlp import trained, read_data, subset, classification_metrics
bundle = trained()
rows = read_data("tickets.json")
report = classification_metrics(bundle["vectorizer"], bundle["baseline"], subset(rows, "test"), bundle["baseline_threshold"])
assert report["count"] == 12 and len(report["confusion_matrix"]) == 3
print({k: v for k, v in report.items() if k != "cases"})
```
