# Solution du challenge

Budget conserve les règlements terminés par identifiant. settle(call,0.003) puis le même appel laisse spent=0.003; settle(call,0.004) déclenche EvidenceError. Pour un système distribué, utiliser un ledger durable et une transaction/clé d’idempotence, pas un simple dictionnaire partagé.

## Vérification exécutable

Les cellules supposent que le lab élève a déjà été exécuté.

```python
from examples.week08.ops import EvidenceError
budget = Budget("0.01")
assert budget.reserve("call-1", "0.008")
assert not budget.reserve("call-2", "0.008")
budget.settle("call-1", "0.003")
budget.settle("call-1", "0.003")
assert budget.spent == Decimal("0.003")
assert budget.reserve("call-3", "0.007")
try:
    budget.settle("call-1", "0.004")
except EvidenceError:
    print("Règlement contradictoire bloqué")
else:
    raise AssertionError("Double règlement accepté")
```
