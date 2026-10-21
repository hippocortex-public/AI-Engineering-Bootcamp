# Solution du challenge

Comparer le résumé à une liste d’unités attendues plutôt qu’aux seuls mots. Marquer la condition comme critique et faire relire son absence. Ne pas ajuster la référence pour rendre le sélecteur meilleur. Les cellules ci-dessous vérifient d’abord les garanties effectivement implémentées : budget et slices.

## Vérification exécutable

Exécuter après les cellules du lab élève.

```python
from examples.week10.nlp import summary_overlap
small = summarize("Une phrase trop longue pour ce budget.", word_budget=1)
assert small["status"] == "budget_exhausted" and small["summary"] == ""
assert summary_overlap("a b", "a c")["f1"] == .5
assert summary_overlap("", "a c")["f1"] == 0
print("Budget et proxy lexical distingués de la fidélité métier")
```
