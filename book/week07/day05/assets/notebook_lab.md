# Exemple exécutable autonome

Ce fragment illustre le concept du jour. Le moteur complet et ses scénarios sont dans examples/week07.

```python
def validate(output):
    assert set(output) == {"category", "draft"}
    assert output["category"] in {"general", "billing"}
    assert isinstance(output["draft"], str) and 0 < len(output["draft"]) <= 2000
    return output
proposal = validate({"category": "general", "draft": "Brouillon à relire"})
assert proposal["draft"] == "Brouillon à relire"
print("Contrat contrôlé; aucune publication")
```
