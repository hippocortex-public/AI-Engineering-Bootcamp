# Challenge — Construire une attention scaled dot-product

## Objectif

Implémenter une fonction `scaled_dot_product_attention(Q, K, V)` en NumPy.

## Contraintes

La fonction doit :

1. accepter trois matrices `Q`, `K`, `V` ;
2. vérifier que les dimensions sont compatibles ;
3. calculer les scores `Q @ K.T` ;
4. appliquer la mise à l'échelle par `sqrt(d_k)` ;
5. appliquer un softmax stable ;
6. retourner la sortie et les poids d'attention.

## Données de test

Utilisez :

```python
Q = np.array([[1.0, 0.0]])
K = np.array([[1.0, 0.0], [0.0, 1.0]])
V = np.array([[10.0, 0.0], [0.0, 5.0]])
```

## Résultat attendu

La première value doit recevoir plus de poids que la deuxième, car la query est mieux alignée avec la première key.

## Extension

Ajoutez un masque causal empêchant une position de regarder les positions futures.
