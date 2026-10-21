# Lab : évaluation reproductible

Python 3.11 ou plus récent. Le moteur et ses tests utilisent uniquement la bibliothèque standard.

Depuis `book/week08/day01/labs` :

```bash
python -m unittest discover -s evaluation_lab/tests -v
python -m evaluation_lab --dataset ../assets/dataset.jsonl --predictions ../assets/baseline.jsonl --output ../assets/baseline_report.json
python -m evaluation_lab --dataset ../assets/dataset.jsonl --predictions ../assets/candidate.jsonl --output ../assets/candidate_report.json
```

La dernière commande termine avec le code 1 : c’est le refus attendu du candidat. Code 0 : règle satisfaite ; code 1 : règle non satisfaite ; code 2 : entrée invalide. Inspecter les rapports plutôt que confondre ce refus avec une panne.

Le parser rejette les identifiants dupliqués, les clés JSON dupliquées et les nombres non finis. Les identifiants inconnus sont invalides. Une sortie absente est un échec. Les objets sont comparés avec une représentation canonique stricte : `true`, `1` et `1.0` diffèrent. L’ordre des clés n’a pas d’effet ; celui des listes en a un.

Les fonctions `evaluate()` et `compare()` sont démontrées dans le notebook. Les empreintes décrivent les données JSON parsées, sans dépendre de l’indentation des fichiers. Les rapports fournis ont été générés par ce moteur.

Pour brancher un vrai modèle : écrire un collecteur séparé produisant une ligne `{ "id": "c01", "output": ... }` par cas, remplacer les entrées descriptives par des scénarios complets, tracer modèle et paramètres, puis faire valider la grille. Ne pas présenter les fixtures comme une expérience sur un modèle.

## Régénérer les notebooks

Depuis la racine du dépôt, dans un environnement dédié :

```bash
python -m pip install -r book/week08/day01/labs/requirements-notebooks.txt
python book/week08/day01/labs/generate_notebooks.py
```

Les notebooks dérivent des Markdown. Modifier d’abord ces sources, puis régénérer. Le notebook retrouve le dépôt en remontant depuis son dossier courant ; ouvrir Jupyter dans le dépôt ou un de ses sous-dossiers.
