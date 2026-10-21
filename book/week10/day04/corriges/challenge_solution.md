# Solution du challenge

Vérifier que les spans originaux sont exacts et non chevauchants, appliquer mask_entities, puis tester un service inconnu comme Facturation Mobile. Son absence de détection est une limite attendue. Conserver le texte source à accès contrôlé si le besoin de revue l’exige.

## Vérification exécutable

Exécuter après les cellules du lab élève.

```python
assert entities("Facturation Mobile ne répond plus.") == []
assert entities("Ne pas utiliser Redis.")[0]["label"] == "TECH"
gold = [{"id":"x", "entities":[{"start":0,"end":12,"label":"SERVICE"}]}]
pred = [{"id":"x", "entities":[{"start":0,"end":8,"label":"SERVICE"}]}]
score = span_metrics(gold,pred)
assert score["false_positive"] == 1 and score["false_negative"] == 1
print("Erreur de frontière et limite du lexique rendues visibles")
```
