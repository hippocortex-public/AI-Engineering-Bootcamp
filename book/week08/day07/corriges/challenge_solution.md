# Solution du challenge

Le rapport baseline est accepté et le candidat échoue uniquement à quality. Avec valid_until au 19 octobre et date au 20 octobre, governance échoue. Avec max_usd_per_success=0.001, cost échoue. Chaque variante conserve les autres preuves et produit un evidence_hash différent.

## Vérification exécutable

Les cellules supposent que le lab élève a déjà été exécuté.

```python
from copy import deepcopy
from examples.week08.demo import load
from examples.week08.ops import assess
expired = deepcopy(load("baseline"))
expired["manifest"]["valid_until"] = "2026-10-19"
assert assess(**expired, day="2026-10-20")["failed_checks"] == ["governance"]
costly = deepcopy(load("baseline"))
costly["policy"]["max_usd_per_success"] = "0.001"
assert assess(**costly, day="2026-10-20")["failed_checks"] == ["cost"]
print("Refus qualité, gouvernance et coût isolés")
```
