# Lab J5 — Reranking, diversité et budget de contexte

Depuis la racine du dépôt :

```bash
python3 book/week09/day05/labs/run.py
python3 -m examples.week09.demo --day 5
```

Résultat attendu : **classements avant/après heuristique; aucun gain universel supposé**.

## Manipulations

1. Reproduire la sortie et retrouver le calcul dans `examples/week09/knowledge.py`.
2. Réaliser l’exercice 2 avec une copie des données, sans modifier le corpus distribué.
3. Vérifier l’invariant étudié et expliquer une limite.

Le corpus se trouve dans `examples/week09/corpus`. Les tests automatisés sont sous `tests/week09`. [QUICKSTART](../../../../docs/week09/QUICKSTART.md) décrit les commandes et les codes retour.

Les modèles locaux et pgvector sont optionnels : lire `examples/week09/optional/README.md` depuis la racine du dépôt. Ils ne sont pas nécessaires pour finir cette journée et ne sont pas présentés comme validés dans cet environnement.
