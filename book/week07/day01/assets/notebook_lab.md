# Exemple exécutable autonome

Ce fragment illustre le concept du jour. Le moteur complet et ses scénarios sont dans examples/week07.

```python
payload = {"event_id": "evt-001", "type": "support.requested"}
accepted = set()
def accept(item):
    is_new = item["event_id"] not in accepted
    accepted.add(item["event_id"])
    return 202 if is_new else 200
assert accept(payload) == 202
assert accept(payload) == 200
print("Un seul identifiant accepté", accepted)
```
