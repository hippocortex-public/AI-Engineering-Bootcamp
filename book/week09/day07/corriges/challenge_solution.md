# Solution du challenge

Utiliser answer sur la question du corpus et citation_valid sur chaque référence. Modifier text d’une copie : elle échoue. La question météo retourne abstain. evaluate_retrieval conserve q8 et les cas par mode. Ne pas annoncer une supériorité de l’hybride si les résultats ne la démontrent pas.

## Vérification exécutable

Exécuter après les cellules du lab élève.

```python
from copy import deepcopy
from examples.week09.knowledge import retrieval_metrics
store = populated()
try:
    result = answer(store, "Comment rejouer un paiement avec Kafka ?", "team-a")
    forged = deepcopy(result["citations"][0])
    forged["text"] = "Une affirmation inventée"
    assert not store.citation_valid(forged, "team-a")
    assert all("MARQUEUR_PRIVE_FICTIF_B" not in c["text"] for c in result["citations"])
finally:
    store.close()
metric = retrieval_metrics(["B", "C", "A"], {"A", "C"}, 2)
assert metric["recall_at_k"] == .5 and metric["mrr_at_k"] == .5
print(metric)
```
