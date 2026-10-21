# Exemple exécutable autonome

Ce fragment illustre le concept du jour. Le moteur complet et ses scénarios sont dans examples/week07.

```python
import json
left = {"event_id": "e1", "text": "Bonjour"}
right = {"text": "Bonjour", "event_id": "e1"}
def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False)
assert canonical(left) == canonical(right)
assert canonical(left) != canonical({**left, "text": "Correction"})
print("Ordre des clés neutralisé, collision de contenu détectable")
```
