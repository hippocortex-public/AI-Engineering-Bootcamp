# Démarrage — Semaine 8

Depuis la racine du dépôt décompressé ou après intégration. Python 3.11 ou plus récent; aucune dépendance pip pour les commandes consolidées ci-dessous.

## 1. Rejouer les deux décisions

```bash
python3 -m examples.week08.demo --day 7 --version baseline
python3 -m examples.week08.demo --day 7 --version candidate
```

La première commande termine avec 0. La seconde termine avec **1 : refus attendu**, et produit un rapport où seul quality échoue. Une entrée mal formée ou une preuve incompatible termine avec 2.

Le replay utilise explicitement le 20 octobre 2026. Pour une autre date, ajouter `--as-of YYYY-MM-DD`. Les approbations fictives expirent après le 20 novembre 2026 inclus : un replay avec une date ultérieure doit refuser governance. La date fournie n’est pas une horloge sécurisée.

Pour écrire le rapport :

```bash
python3 -m examples.week08.demo --day 7 --version candidate --output /tmp/week08-candidate.json
```

Le fichier est produit même lorsque la commande retourne 1. La commande n’envoie aucun message et n’effectue aucun déploiement.

## 2. Parcourir les journées

```bash
python3 book/week08/day02/labs/run.py
python3 -m examples.week08.demo --day 3 --version candidate
python3 -m examples.week08.demo --day 4 --version baseline
python3 -m examples.week08.demo --day 5 --version baseline
python3 -m examples.week08.demo --day 6 --version baseline
```

Les fichiers `labs/run.py` existent pour J2 à J7. J1 conserve son interface d’origine :

```bash
cd book/week08/day01/labs
python3 -m evaluation_lab --dataset ../assets/dataset.jsonl --predictions ../assets/baseline.jsonl --output /tmp/week08-j1-baseline.json
```

Revenir à la racine pour toutes les commandes suivantes.

## 3. Notebooks

```bash
python3 scripts/generate_week08_notebooks.py
```

Le générateur consolidé utilise la bibliothèque standard et reproduit les notebooks J1 à l’identique depuis le Markdown. L’ancien générateur propre à J1 est conservé, avec ses dépendances optionnelles d’origine; il n’est pas nécessaire pour cette commande.

Ouvrir Jupyter depuis la racine du dépôt ou un de ses sous-dossiers. Les notebooks élève sont sous notebooks/week08; les enseignants sous notebooks/week08/teacher. Les cellules enseignant du challenge s’exécutent après les cellules du lab élève. L’affichage des diagrammes Mermaid dépend du lecteur; les sources .mmd restent disponibles.

## 4. Contrôles

```bash
python3 scripts/validate_week08.py
python3 -m unittest discover -s tests/week08 -v
```

Pour les tests J1 d’origine, depuis la racine :

```bash
python3 - <<'PY'
from pathlib import Path
import subprocess
import sys
lab = Path('book/week08/day01/labs')
raise SystemExit(subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'evaluation_lab/tests', '-v'], cwd=lab).returncode)
PY
```

## 5. Régénérer le projet de supervision

```bash
python3 scripts/make_week08_reports.py
```

Cette commande recalcule deux rapports JSON, un export de télémétrie illustratif, la comparaison Markdown et une vue HTML statique dans docs/week08/reports. Ouvrir supervision.html dans un navigateur pour lire le résultat; aucune ressource réseau n’est requise. L’HTML est un rapport, pas une console de production ni une application d’administration.

Pour reproduire les observations synthétiques d’origine : `python3 scripts/make_week08_fixtures.py`. Cette commande réécrit volontairement les fixtures S8 générées, sans toucher au dataset ni aux sorties J1. Conserver vos expériences dans des copies avant de la lancer.
