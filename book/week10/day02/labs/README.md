# Lab J2 — Extraction structurée, valeurs et ambiguïtés

Depuis la racine du dépôt, dans l’environnement S10 :

```bash
python3 book/week10/day02/labs/run.py
python3 -m examples.week10.demo --day 2
```

Résultat attendu : **16 valeurs et 16 statuts comparés, avec deux champs ambigus dans e4**.

## Travail

1. Exécuter le scénario et identifier la nature de chaque composant : appris, adapté ou à règles.
2. Réaliser l’exercice 2 sur une copie, sans modifier le corpus distribué.
3. Expliquer le dénominateur du résultat et une limite.

Les données sont sous `examples/week10/data`; le code commun sous `examples/week10/nlp.py`; les tests sous `tests/week10`. Lire [QUICKSTART](../../../../docs/week10/QUICKSTART.md) pour les dépendances, artefacts et commandes.

Les modèles entraînés sont conservés en mémoire dans chaque processus pour accélérer les notebooks. Une modification des données demande un nouveau processus ou de vider explicitement les caches trained/specialized avant de réentraîner. Les correctifs du notebook enseignant s’exécutent après le lab élève.
