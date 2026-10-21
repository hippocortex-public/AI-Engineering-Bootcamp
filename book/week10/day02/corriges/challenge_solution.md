# Solution du challenge

Utiliser une même syntaxe reconnue latence de N ms. L’absence donne missing; deux mentions de 100 ms donnent present avec deux preuves; 100 puis 200 ms donnent ambiguous. Chaque preuve doit être un slice exact du texte source.

## Vérification exécutable

Exécuter après les cellules du lab élève.

```python
assert extract("Aucune mesure disponible.")["duration_ms"]["status"] == "missing"
same = extract("La latence de 100 ms puis la latence de 100 ms.")["duration_ms"]
assert same["status"] == "present" and len(same["evidence"]) == 2
different = extract("La latence de 100 ms puis la latence de 200 ms.")["duration_ms"]
assert different["status"] == "ambiguous" and different["value"] is None
assert extract("La latence de 0,25 ms.")["duration_ms"]["value"] == "0.25"
```
