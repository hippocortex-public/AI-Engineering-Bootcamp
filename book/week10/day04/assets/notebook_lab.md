# Lab exécutable

NumPy et scikit-learn sont requis; aucune requête réseau dans les cellules.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week10/nlp.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from examples.week10.nlp import read_data, entities, span_metrics, mask_entities
examples = read_data("examples.json")
predicted = [{"id":r["id"], "entities":entities(r["text"])} for r in examples]
metrics = span_metrics(examples, predicted)
assert metrics["true_positive"] == 12
for row in examples:
    assert all(row["text"][s["start"]:s["end"]] == s["text"] for s in entities(row["text"]))
print(metrics)
print(mask_entities(examples[0]["text"], predicted[0]["entities"]))
```
