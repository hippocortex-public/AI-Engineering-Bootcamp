# Corrigé — Challenge Jour 3

Voir l'implémentation complète dans :

```text
book/week01/day03/labs/scaled_dot_product_attention.py
```

## Solution principale

```python
import math
import numpy as np

def stable_softmax(x, axis=-1):
    shifted = x - np.max(x, axis=axis, keepdims=True)
    exp = np.exp(shifted)
    return exp / np.sum(exp, axis=axis, keepdims=True)

def scaled_dot_product_attention(Q, K, V, mask=None):
    Q = np.asarray(Q, dtype=float)
    K = np.asarray(K, dtype=float)
    V = np.asarray(V, dtype=float)

    if Q.ndim != 2 or K.ndim != 2 or V.ndim != 2:
        raise ValueError("Q, K and V must be 2D matrices.")
    if Q.shape[1] != K.shape[1]:
        raise ValueError("Q and K must have the same feature dimension.")
    if K.shape[0] != V.shape[0]:
        raise ValueError("K and V must have the same sequence length.")

    d_k = K.shape[1]
    scores = (Q @ K.T) / math.sqrt(d_k)

    if mask is not None:
        scores = np.where(mask, scores, -1e9)

    weights = stable_softmax(scores, axis=-1)
    output = weights @ V
    return output, weights
```

## Explication

- `Q @ K.T` calcule l'alignement entre chaque query et chaque key.
- La division par `sqrt(d_k)` stabilise les scores.
- Le softmax transforme les scores en poids.
- `weights @ V` agrège les values selon ces poids.
