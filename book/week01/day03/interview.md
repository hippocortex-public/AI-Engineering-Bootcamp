# Préparation entretien — Transformer et Attention

## Question 1

Expliquez l'attention à une personne technique qui ne connaît pas les Transformers.

### Réponse attendue

L'attention est un mécanisme qui permet à chaque token d'une séquence de pondérer les autres tokens selon leur utilité. On calcule des scores entre queries et keys, on les normalise avec un softmax, puis on agrège les values selon ces poids.

## Question 2

Pourquoi divise-t-on les scores par `sqrt(d_k)` ?

### Réponse attendue

Quand la dimension augmente, les produits scalaires peuvent devenir grands. Le softmax peut alors saturer, produire des distributions trop extrêmes et rendre l'apprentissage moins stable. La division par `sqrt(d_k)` stabilise les scores.

## Question 3

Quelle est la différence entre self-attention et cross-attention ?

### Réponse attendue

En self-attention, queries, keys et values proviennent de la même séquence. En cross-attention, les queries proviennent d'une séquence et les keys/values d'une autre, par exemple dans un modèle encodeur-décodeur.

## Question 4

Pourquoi l'attention complète coûte-t-elle cher ?

### Réponse attendue

Parce qu'elle compare chaque token à chaque autre token. Pour `n` tokens, il faut calculer `n²` scores d'attention.

## Question 5

Est-ce qu'une matrice d'attention explique complètement la décision d'un modèle ?

### Réponse attendue

Non. Elle peut donner un signal d'inspection, mais ce n'est pas toujours une explication causale complète. Les représentations internes, les couches suivantes et les interactions non linéaires influencent aussi la sortie.

## Question 6

Pourquoi les Transformers sont-ils importants pour les LLM ?

### Réponse attendue

Ils permettent un entraînement massif plus parallélisable, capturent des dépendances longues et utilisent efficacement les représentations contextualisées. Ils sont devenus la base de nombreux LLM modernes.
