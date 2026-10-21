# Lab exécutable

NumPy et scikit-learn sont requis; aucune requête réseau dans les cellules.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week10/nlp.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from examples.week10.nlp import specialized, embedding_report
projection, details = specialized()
report = embedding_report()
assert report["queries"] == 12 and report["index_documents"] == 36
assert report["modes"]["supervised_nca"]["dimension"] == 8
print({mode:{key:value for key,value in metrics.items() if key != "cases"} for mode,metrics in report["modes"].items()})
print(details)
```
