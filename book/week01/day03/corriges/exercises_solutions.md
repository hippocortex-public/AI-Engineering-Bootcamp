# Corrigés — Exercices Jour 3

## Exercice 1 — Q, K, V

Une Query représente ce qu'un token cherche dans le contexte. Une Key représente ce qu'un token rend disponible pour être retrouvé. Une Value contient l'information effectivement agrégée si ce token est sélectionné.

Exemple : dans `Le serveur répond lentement car il est saturé`, le token `il` peut avoir une query qui cherche un antécédent. Les tokens `serveur` et `lentement` ont des keys différentes. Si `serveur` obtient un score élevé, sa value contribue fortement à la représentation contextualisée de `il`.

## Exercice 2 — Produit scalaire

```text
Q · K1 = [1, 0] · [1, 0] = 1
Q · K2 = [1, 0] · [0, 1] = 0
```

`K1` est plus alignée avec `Q` que `K2`.

## Exercice 3 — Softmax simple

Le score `2.0` recevra le plus d'attention, car le softmax attribue une probabilité plus grande aux valeurs les plus élevées. Les trois scores deviendront des poids positifs qui somment à 1.

## Exercice 4 — Coût quadratique

- 10 tokens : `10 × 10 = 100` scores
- 100 tokens : `100 × 100 = 10 000` scores
- 1 000 tokens : `1 000 × 1 000 = 1 000 000` scores

La conséquence est que la mémoire et le calcul augmentent très vite avec la longueur de séquence. Une longue fenêtre de contexte peut donc coûter cher en latence et en ressources.

## Exercice 5 — Analyse d'architecture

Un RNN traite généralement les éléments dans l'ordre, car chaque étape dépend de l'état précédent. Un Transformer calcule les relations entre positions via des opérations matricielles qui peuvent être parallélisées sur GPU.

## Exercice 6 — Cas produit

Avantages :

- un modèle pré-entraîné comprend déjà beaucoup de structures linguistiques ;
- il peut être adapté rapidement à des tickets variés sans entraîner un modèle depuis zéro.

Risques :

- coût d'inférence élevé si le volume est important ;
- hallucinations ou résumés incomplets si le prompt et l'évaluation sont insuffisants.

## Exercice 7 — Lecture de matrice d'attention

La première ligne indique comment le premier token distribue son attention :

- 70 % sur lui-même ou la position 1 ;
- 20 % sur la position 2 ;
- 10 % sur la position 3.

Cela signifie que sa représentation de sortie dépend principalement de la première value.
