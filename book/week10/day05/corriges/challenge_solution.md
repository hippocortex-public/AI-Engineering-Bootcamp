# Solution du challenge

artifact fournit une empreinte et les paramètres sans pickle. predict_artifact reconstitue TF-IDF et le calcul logistique one-vs-rest. Comparer les probabilités à une tolérance numérique, vérifier l’intégrité après modification d’un poids et conserver le résultat même si les F1 sont égaux.

## Vérification exécutable

Exécuter après les cellules du lab élève.

```python
import math
from copy import deepcopy
from examples.week10.nlp import ContractError
text = "Le jeton a expiré et la connexion est refusée."
loaded = predict_artifact(candidate, text)
live = classify(text, bundle, "adapted")
assert loaded["label"] == live["label"]
assert math.isclose(loaded["max_probability"], live["max_probability"], rel_tol=1e-10)
changed = deepcopy(candidate)
changed["coef"][0][0] += .1
try:
    predict_artifact(changed, text)
except ContractError:
    print("Poids modifiés sans empreinte correspondante refusés")
else:
    raise AssertionError("Artefact modifié accepté")
```
