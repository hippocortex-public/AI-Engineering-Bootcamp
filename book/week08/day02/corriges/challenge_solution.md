# Solution du challenge

Appeler benchmark(runs, ids, repeats=4) : EvidenceError. Pour un essai réel, fixer corpus réservé, versions, concurrence et rythme d’arrivée, borne de requêtes, coût maximal et arrêt sur erreurs. Mesurer le temps mur et tracer cache/équipement. Ne pas inventer de nouvelles observations à partir des fixtures.

## Vérification exécutable

Les cellules supposent que le lab élève a déjà été exécuté.

```python
try:
    benchmark(data["runs"][:-1], ids)
except EvidenceError:
    print("Couverture incomplète bloquée")
else:
    raise AssertionError("Le benchmark a accepté un essai absent")
```
