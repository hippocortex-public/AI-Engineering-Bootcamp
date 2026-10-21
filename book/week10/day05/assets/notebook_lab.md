# Lab exécutable

NumPy et scikit-learn sont requis; aucune requête réseau dans les cellules.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week10/nlp.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from examples.week10.nlp import trained, artifact, classify, predict_artifact
bundle = trained()
base = artifact(bundle, "baseline")
candidate = artifact(bundle, "adapted")
assert base["vocabulary"] == candidate["vocabulary"]
assert base["idf"] == candidate["idf"]
assert base["coef"] != candidate["coef"]
print(bundle["selection"], "selected:", bundle["selected_epochs"])
```
