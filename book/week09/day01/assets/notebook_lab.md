# Lab exécutable

Les cellules s’exécutent hors ligne depuis l’arbre du dépôt.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week09/knowledge.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from examples.week09.demo import documents
from examples.week09.knowledge import chunk_document, ContractError
doc = documents()[0]
chunks = chunk_document(doc, max_words=24, overlap=4)
assert chunks and all(doc["text"][c["start"]:c["end"]] == c["text"] for c in chunks)
assert len({c["chunk_id"] for c in chunks}) == len(chunks)
print({"chunks": len(chunks), "first": chunks[0]})
```
