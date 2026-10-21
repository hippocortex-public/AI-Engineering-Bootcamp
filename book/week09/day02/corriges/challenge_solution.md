# Solution du challenge

Vérifier l’égalité des vecteurs de Kafka paiement et paiement Kafka; tester cosine([1,0],[1]) et attendre ContractError. Pour les synonymes, annoter des paraphrases et distracteurs sur un jeu réservé, comparer hashbow et un modèle local, puis publier erreurs et configuration. Aucun résultat neuronal ne peut être déduit du test lexical.

## Vérification exécutable

Exécuter après les cellules du lab élève.

```python
try:
    cosine([1, 0], [1])
except ContractError:
    print("Espaces incompatibles refusés")
else:
    raise AssertionError("Dimension incompatible acceptée")
assert encoder.encode("le et une") == [0.0] * 128
print("Ordre perdu et vecteur nul vérifiés")
```
