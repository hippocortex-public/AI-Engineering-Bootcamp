# Lab J2 — Benchmarks reproductibles et variabilité

Depuis la racine du dépôt :

```bash
python3 book/week08/day02/labs/run.py
python3 -m examples.week08.demo --day 2 --version baseline
```

Résultat attendu : **36 essais par version; p95 baseline 601 ms, candidat 461 ms; maximum candidat 2200 ms**.

## Manipulation

1. Reproduire la sortie et identifier les fixtures utilisées.
2. Expliquer le nombre d’observations et le dénominateur du résultat.
3. Effectuer l’exercice 2 sans modifier les fixtures distribuées : charger une copie en mémoire.
4. Conserver la différence de résultat et sa cause.

Le code commun est dans `examples/week08/ops.py`; les observations et politiques sont dans `examples/week08/fixtures`. Le dataset et les réponses de qualité restent ceux de J1. Les scripts sont indépendants de n8n et de tout fournisseur.

Pour le projet complet et les codes de retour, lire [QUICKSTART](../../../../docs/week08/QUICKSTART.md). Les assertions du notebook enseignant complètent la solution du challenge.
