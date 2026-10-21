# Solution du challenge

Utiliser un document valide et chunk_document(max_words=4, overlap=1). Les fenêtres attendues portent les mots 0–3, 3–6 et 6–9. Vérifier chaque slice dans le texte original et comparer les identifiants de deux appels. Tester aussi overlap=4 : la configuration doit être refusée.

## Vérification exécutable

Exécuter après les cellules du lab élève.

```python
small = {**doc, "text": "zero un deux trois quatre cinq six sept huit neuf"}
windows = chunk_document(small, 4, 1)
assert [c["text"] for c in windows] == ["zero un deux trois", "trois quatre cinq six", "six sept huit neuf"]
assert [c["chunk_id"] for c in windows] == [c["chunk_id"] for c in chunk_document(small, 4, 1)]
try:
    chunk_document(small, 4, 4)
except ContractError:
    print("Overlap non progressif refusé")
else:
    raise AssertionError("Configuration invalide acceptée")
```
