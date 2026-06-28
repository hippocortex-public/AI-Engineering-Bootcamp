# Exercices — Transformer et Attention

## Exercice 1 — Q, K, V

Expliquez avec vos mots la différence entre Query, Key et Value.

Contraintes :

- ne pas utiliser uniquement une définition mathématique ;
- donner un exemple avec une phrase ;
- préciser pourquoi les trois représentations sont utiles.

## Exercice 2 — Produit scalaire

On donne :

```text
Q = [1, 0]
K1 = [1, 0]
K2 = [0, 1]
```

Calculez les scores bruts entre `Q` et chaque key.

## Exercice 3 — Softmax simple

On donne les scores :

```text
[2.0, 1.0, 0.0]
```

Sans chercher une précision parfaite, indiquez quel élément recevra le plus d'attention et pourquoi.

## Exercice 4 — Coût quadratique

Combien de scores contient une matrice d'attention pour :

- 10 tokens ;
- 100 tokens ;
- 1 000 tokens ?

Expliquez la conséquence pour une fenêtre de contexte très longue.

## Exercice 5 — Analyse d'architecture

Pourquoi un Transformer est-il plus facile à paralléliser qu'un RNN classique ?

## Exercice 6 — Cas produit

Vous construisez un assistant interne qui résume des tickets support. Les tickets sont courts, mais très nombreux.

Indiquez deux raisons pour lesquelles un modèle Transformer pré-entraîné peut être utile, et deux risques opérationnels à surveiller.

## Exercice 7 — Lecture de matrice d'attention

On observe la matrice suivante :

```text
[
  [0.70, 0.20, 0.10],
  [0.10, 0.80, 0.10],
  [0.30, 0.30, 0.40]
]
```

Que signifie la première ligne ?
