# Lab exécutable

NumPy et scikit-learn sont requis; aucune requête réseau dans les cellules.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week10/nlp.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from examples.week10.nlp import summarize, read_data
example = read_data("examples.json")[0]
result = summarize(example["text"], max_sentences=2, word_budget=45)
assert result["word_count"] <= 45
assert len(result["sentences"]) <= 2
assert all(example["text"][s["start"]:s["end"]] == s["text"] for s in result["sentences"])
assert [s["start"] for s in result["sentences"]] == sorted(s["start"] for s in result["sentences"])
print(result["summary"])
```
