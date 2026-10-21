# Solution du challenge

Cette fonction ajoute des exigences ; elle conserve la décision globale et les refus critiques. Une catégorie absente échoue plutôt que d’être ignorée.

```python
import math

def segment_gate(report, thresholds):
    if not isinstance(thresholds, dict) or not thresholds:
        raise ValueError("thresholds required")
    for category, threshold in thresholds.items():
        if not isinstance(category, str) or not category.strip():
            raise ValueError("invalid category")
        if type(threshold) not in (int, float) or not math.isfinite(threshold) or not 0 <= threshold <= 1:
            raise ValueError("invalid threshold")
    return report["accepted"] and all(
        category in report["segments"] and report["segments"][category]["rate"] >= threshold
        for category, threshold in thresholds.items()
    )

assert segment_gate(baseline, {"support": 0.6})
assert not segment_gate(baseline, {"support": 0.8})
assert not segment_gate(candidate, {"support": 0.8})
assert not segment_gate(baseline, {"unknown": 0.5})
for invalid in ({}, {"support": True}, {"support": float("nan")}, {"support": 1.1}):
    try:
        segment_gate(baseline, invalid)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid configuration accepted")
print("Challenge : 8 assertions validées")
```

Le groupe support contient cinq cas. Trois réussissent dans la baseline, soit 0,6. Le seuil de 0,8 demande quatre réussites. Ce seuil illustratif doit être justifié par le besoin produit ; il n’est pas une estimation fiable du taux réel sur seulement cinq cas.
