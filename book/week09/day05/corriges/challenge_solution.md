# Solution du challenge

Parcourir les candidats classés, garder un ensemble de doc_id vus et ajouter seulement les passages entiers qui tiennent dans le budget. Ne marquer un document comme vu qu’après son ajout. Comparer les sources et la couverture; ne pas imposer cette règle à tous les cas sans mesure.

## Vérification exécutable

Exécuter après les cellules du lab élève.

```python
def diverse_pack(items, budget):
    seen = set()
    result = []
    used = 0
    for item in items:
        size = len(item["text"].split())
        if item["doc_id"] not in seen and used + size <= budget:
            seen.add(item["doc_id"])
            used += size
            result.append(item)
    return result
assert [c["chunk_id"] for c in diverse_pack(candidates, 8)] == ["medium"]
print("La diversité peut aussi supprimer un passage complémentaire")
```
