# Solution du challenge

RRF([A,B],[B,A]) attribue la même somme à A et B; l’identifiant départage le tri. C au rang 3 d’une seule liste vaut 1/(60+3). Injecter deux fois le même identifiant dans une liste doit produire ContractError.

## Vérification exécutable

Exécuter après les cellules du lab élève.

```python
try:
    rrf([[A, A]])
except ContractError:
    print("Double contribution dans une même liste bloquée")
else:
    raise AssertionError("Doublon accepté")
from examples.week09.demo import populated, evaluate_retrieval
store = populated()
try:
    print(evaluate_retrieval(store)["summaries"])
finally:
    store.close()
```
