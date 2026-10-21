# Solution du challenge

Modifier une copie du texte test en y ajoutant un mot unique, réentraîner avec train_bundle puis vérifier son absence de vocabulary_. Les données de sélection ne changent pas. Pour le groupe partagé, modifier un group_id test avec celui du train : validate_dataset lève ContractError avant tout entraînement.

## Vérification exécutable

Exécuter après les cellules du lab élève.

```python
from copy import deepcopy
from examples.week10.nlp import validate_dataset, ContractError
changed = deepcopy(rows)
first_train = next(r for r in changed if r["split"] == "train")
first_test = next(r for r in changed if r["split"] == "test")
first_test["group_id"] = first_train["group_id"]
try:
    validate_dataset(changed)
except ContractError:
    print("Fuite de groupe refusée")
else:
    raise AssertionError("Groupe partagé accepté")
from examples.week10.nlp import train_bundle
reserved = deepcopy(rows)
for row in reserved:
    if row["split"] == "test":
        row["text"] += " termeuniquedutest"
retrained = train_bundle(reserved)
assert "termeuniquedutest" not in retrained["vectorizer"].vocabulary_
assert retrained["vectorizer"].vocabulary_ == bundle["vectorizer"].vocabulary_
```
