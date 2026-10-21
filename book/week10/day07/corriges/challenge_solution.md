# Solution du challenge

Le cas e4 impose la revue à cause des conflits de code et de durée. Recharger baseline/adapted et comparer à l’inférence en mémoire. Conserver l’absence de gain de F1. Une prochaine expérience peut cibler les tickets hors distribution, les entités inconnues ou des résumés omettant un fait critique, avec une grille et un jeu réservé.

## Vérification exécutable

Exécuter après les cellules du lab élève.

```python
from examples.week10.nlp import trained, artifact, predict_artifact, classify
bundle = trained()
for variant in ("baseline", "adapted"):
    saved = artifact(bundle, variant)
    for row in examples:
        loaded = predict_artifact(saved, row["text"])
        live = classify(row["text"], bundle, variant)
        assert loaded["label"] == live["label"]
print("Les deux artefacts reproduisent les décisions en mémoire")
```
