# Lab exécutable

NumPy et scikit-learn sont requis; aucune requête réseau dans les cellules.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week10/nlp.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from examples.week10.nlp import read_data, process
examples = read_data("examples.json")
results = [{"id":row["id"], **process(row["text"])} for row in examples]
ambiguous = next(row for row in results if row["id"] == "e4")
assert ambiguous["requires_review"]
assert ambiguous["fields"]["http_status"]["status"] == "ambiguous"
print([{ "id":r["id"], "classification":r["classification"]["label"], "review":r["requires_review"]} for r in results])
```
