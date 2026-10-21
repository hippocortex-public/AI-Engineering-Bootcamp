# Lab exécutable

Les cellules s’exécutent hors ligne depuis l’arbre du dépôt.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week09/knowledge.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from examples.week09.knowledge import context_pack, rerank
candidates = [
    {"chunk_id": "long", "doc_id": "D1", "text": "un deux trois quatre cinq six sept huit neuf", "title": "", "score": .9},
    {"chunk_id": "medium", "doc_id": "D2", "text": "un deux trois quatre cinq", "title": "", "score": .8},
    {"chunk_id": "short", "doc_id": "D2", "text": "un deux trois", "title": "", "score": .7},
]
packed = context_pack(candidates, word_budget=8)
assert [c["chunk_id"] for c in packed] == ["medium", "short"]
ranked = rerank("quatre cinq", candidates)
assert ranked[0]["term_coverage"] == 1
print([c["chunk_id"] for c in ranked])
```
