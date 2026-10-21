# Lab exécutable

NumPy et scikit-learn sont requis; aucune requête réseau dans les cellules.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week10/nlp.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from examples.week10.nlp import extract, read_data
examples = read_data("examples.json")
for example in examples:
    result = extract(example["text"])
    for key, field in result.items():
        assert field["value"] == example["expected"][key]
        assert field["status"] == example["expected_status"][key]
        assert all(example["text"][e["start"]:e["end"]] == e["text"] for e in field["evidence"])
print("16 valeurs et 16 statuts vérifiés")
```
