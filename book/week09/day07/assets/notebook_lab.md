# Lab exécutable

Les cellules s’exécutent hors ligne depuis l’arbre du dépôt.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week09/knowledge.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from examples.week09.demo import populated, evaluate_retrieval
from examples.week09.knowledge import answer
store = populated()
try:
    response = answer(store, "Comment rejouer un paiement avec Kafka ?", "team-a")
    assert response["status"] == "supported_extract" and response["citations"]
    assert all(store.citation_valid(c, "team-a") for c in response["citations"])
    assert answer(store, "Quelle météo demain à Oslo ?", "team-a")["status"] == "abstain"
    report = evaluate_retrieval(store)
    assert report["queries"] == 8
    print(response["answer"])
    print(report["summaries"])
finally:
    store.close()
```
