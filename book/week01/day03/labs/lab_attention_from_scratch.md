# Lab — Attention from scratch

## Objectif

Construire une attention scaled dot-product avec NumPy et inspecter les poids produits.

## Étape 1 — Installer les dépendances

Le lab utilise uniquement NumPy.

```bash
pip install numpy
```

## Étape 2 — Exécuter le script

Depuis la racine du dépôt :

```bash
python book/week01/day03/labs/scaled_dot_product_attention.py
```

## Étape 3 — Observer les poids

Le script affiche :

- la matrice des poids d'attention ;
- la sortie contextualisée ;
- une vérification que chaque ligne somme à 1.

## Étape 4 — Tester un masque causal

Le masque causal empêche une position de regarder les positions futures. Il est utile pour les modèles autoregressifs.

## Étape 5 — Exécuter les tests

```bash
pytest tests/week01/day03
```

## Questions d'analyse

1. Pourquoi les lignes des poids d'attention somment-elles à 1 ?
2. Que se passe-t-il si `Q` est très aligné avec une key ?
3. Pourquoi un masque causal est-il nécessaire pour générer du texte token par token ?
4. Quel est l'impact du coût `O(n²)` sur une longue séquence ?
