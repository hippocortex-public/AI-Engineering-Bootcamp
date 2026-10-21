# Solution du challenge

Créer une copie indépendante du manifeste pour chaque mutation. Vérifier respectivement reviewer_not_authorized, separation_of_duties, approval_missing et approval_expired. Ne pas muter la fixture partagée entre essais. Un statut refusé ne doit pas devenir une erreur technique indistincte.

## Vérification exécutable

Les cellules supposent que le lab élève a déjà été exécuté.

```python
mutations = [({"reviewer": "unknown"}, "reviewer_not_authorized"),
             ({"owner": "reviewer-demo"}, "separation_of_duties"),
             ({"approved": False}, "approval_missing"),
             ({"valid_until": "2026-10-19"}, "approval_expired")]
for patch, expected in mutations:
    candidate = {**deepcopy(data["manifest"]), **patch}
    decision = govern(candidate, config_hash, data["policy"], "2026-10-20")
    assert not decision["accepted"] and expected in decision["reasons"]
print("Quatre causes de refus vérifiées")
```
