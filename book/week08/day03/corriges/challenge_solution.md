# Solution du challenge

Le dénominateur est len(runs), le numérateur est sum(r[status]==ok et r[duration_ms]<1000). Retourner 35/36 pour le candidat, refuser le lot vide. Le runbook vérifie d’abord le périmètre et la version, puis les erreurs, les traces et la dépendance lente; définir la condition de rollback.

## Vérification exécutable

Les cellules supposent que le lab élève a déjà été exécuté.

```python
def batch_sli(rows):
    if not rows:
        raise ValueError("Lot vide")
    return sum(r["status"] == "ok" and r["duration_ms"] < 1000 for r in rows) / len(rows)
assert batch_sli(runs) == 35 / 36
try:
    batch_sli([])
except ValueError:
    print("Absence de données distinguée d’un SLI parfait")
else:
    raise AssertionError("Lot vide accepté")
```
