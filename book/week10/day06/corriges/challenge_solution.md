# Solution du challenge

embedding_report conserve les ids des voisins de chaque requête. Comparer les cas par id, pas les lignes par position supposée. Une différence indique un changement de géométrie, sans prouver que le ticket retrouvé fournit une réponse utile. Les labels de thèmes sont la seule pertinence du lab.

## Vérification exécutable

Exécuter après les cellules du lab élève.

```python
import math
for mode in report["modes"].values():
    for case in mode["cases"]:
        assert len(case["ranked_ids"]) == 3
        assert all("-train-" in value for value in case["ranked_ids"])
        assert case["recall_at_3"] <= .25 + 1e-12
        assert math.isclose(case["recall_at_3"], case["precision_at_3"] / 4, rel_tol=1e-10, abs_tol=1e-10)
print("Index distinct du test et dénominateur de rappel vérifiés")
```
