# Exemple exécutable autonome

Ce fragment illustre le concept du jour. Le moteur complet et ses scénarios sont dans examples/week07.

```python
transitions = {"received": {"awaiting_review", "retry", "dead_letter"},
               "awaiting_review": {"published", "rejected", "expired"}}
def move(current, target):
    if target not in transitions.get(current, set()):
        raise ValueError("Transition interdite")
    return target
assert move("received", "awaiting_review") == "awaiting_review"
try:
    move("received", "published")
except ValueError:
    print("Publication directe bloquée")
else:
    raise AssertionError("Transition dangereuse")
```
