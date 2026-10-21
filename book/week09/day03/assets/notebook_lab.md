# Lab exécutable

Les cellules s’exécutent hors ligne depuis l’arbre du dépôt.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week09/knowledge.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
import tempfile
from pathlib import Path
from examples.week09.demo import populated
from examples.week09.knowledge import Store
with tempfile.TemporaryDirectory() as directory:
    path = str(Path(directory) / "index.sqlite")
    store = populated(path)
    before = store.search("paiement Kafka", "team-a", top_k=3)
    store.close()
    reopened = Store(path)
    try:
        after = reopened.search("paiement Kafka", "team-a", top_k=3)
        assert [c["chunk_id"] for c in before] == [c["chunk_id"] for c in after]
        assert all(c["tenant"] == "team-a" for c in after)
    finally:
        reopened.close()
print("Persistance et filtre vérifiés")
```
