# Exemple exécutable autonome

Ce fragment illustre le concept du jour. Le moteur complet et ses scénarios sont dans examples/week07.

```python
import hashlib
import json
proposal = {"category": "general", "draft": "Version A"}
def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
approved_hash = digest(proposal)
changed = {**proposal, "draft": "Version B"}
assert digest(changed) != approved_hash
print("Une validation de A n’autorise pas B")
```
