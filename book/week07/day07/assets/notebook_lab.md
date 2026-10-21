# Exemple exécutable autonome

Ce fragment illustre le concept du jour. Le moteur complet et ses scénarios sont dans examples/week07.

```python
states = ["published", "rejected", "expired"]
publications = ["evt-approved"]
assert states.count("published") == len(publications) == 1
assert "rejected" in states and "expired" in states
print({"states": states, "local_publications": len(publications)})
```
