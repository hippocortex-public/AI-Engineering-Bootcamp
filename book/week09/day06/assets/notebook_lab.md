# Lab exécutable

Les cellules s’exécutent hors ligne depuis l’arbre du dépôt.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week09/knowledge.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from examples.week09.demo import populated
store = populated()
try:
    store.remember("team-a", "alice", "s1", "style", "Réponse courte", ttl=60, now=1000)
    assert len(store.recall("team-a", "alice", "s1", now=1001)) == 1
    assert store.recall("team-a", "bob", "s1", now=1001) == []
    assert store.recall("team-a", "alice", "s2", now=1001) == []
    assert store.recall("team-a", "alice", "s1", now=1060) == []
finally:
    store.close()
print("Isolation et expiration exactes vérifiées")
```
