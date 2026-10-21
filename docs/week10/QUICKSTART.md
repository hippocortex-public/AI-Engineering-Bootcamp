# Démarrage — Semaine 10

Commandes depuis la racine du dépôt décompressé ou après intégration. Python 3.11 ou plus récent; l’environnement validé utilise Python 3.12. Les bibliothèques obligatoires sont épinglées aux versions exécutées. Aucun poids de modèle ni clé API n’est requis.

## 1. Environnement isolé

```bash
python3 -m venv /tmp/bootcamp-s10-venv
. /tmp/bootcamp-s10-venv/bin/activate
python -m pip install -r examples/week10/requirements.txt
```

L’installation peut nécessiter le réseau ou un dépôt de paquets local. Les scénarios et notebooks n’appellent ensuite aucun service externe. Ne pas écraser les dépendances globales du dépôt; l’environnement est dédié à S10.

## 2. Projet et scénarios

```bash
python -m examples.week10.demo --day 7
python book/week10/day01/labs/run.py
python -m examples.week10.demo --day 2
python -m examples.week10.demo --day 3
python -m examples.week10.demo --day 4
python -m examples.week10.demo --day 5
python -m examples.week10.demo --day 6
```

Chaque journée possède son labs/run.py. Les entraînements sont petits et s’exécutent sur CPU. Le processus conserve les modèles en cache pour éviter de réentraîner dans chaque cellule de notebook; un nouveau processus recalcule l’expérience.

Analyser un texte :

```bash
python -m examples.week10.demo --text "INC-204 concerne Paiement API en prod. Le jeton expiré provoque HTTP 401."
```

Code 0 : analyse sans revue selon la règle locale; code 1 : revue requise; code 2 : entrée/option invalide. Une revue n’est pas une panne. Un conflit de champs ou un ticket_id manquant peut imposer la revue même si la classification est acceptée. La sortie ne déclenche aucune action métier.

Pour enregistrer une analyse :

```bash
python -m examples.week10.demo --text "INC-204 retourne HTTP 401 et HTTP 503." --output /tmp/s10-analysis.json
```

## 3. Notebooks et contrôles

```bash
python scripts/generate_week10_notebooks.py
python scripts/validate_week10.py
python -m unittest discover -s tests/week10 -v
```

Le générateur utilise la bibliothèque standard; les cellules exigent les dépendances S10. Ouvrir Jupyter dans l’arbre du dépôt. Les cellules de correction enseignant s’exécutent après le lab élève. Les diagrammes Mermaid restent disponibles en .mmd si le lecteur ne les rend pas.

## 4. Rapports et artefacts

```bash
python scripts/make_week10_reports.py
```

Les fichiers de docs/week10/reports incluent mesures de classification/adaptation, extraction, résumé, NER, embeddings, analyse intégrée et versions logicielles. Deux artefacts JSON permettent une inférence de classification sans pickle. La projection NCA est exportée avec sa provenance pour inspection.

```python
import json
from pathlib import Path
from examples.week10.nlp import predict_artifact

saved = json.loads(Path('docs/week10/reports/adapted_classifier.json').read_text())
print(predict_artifact(saved, 'Le jeton a expiré et la connexion est refusée.'))
```

Cette relecture ne réentraîne pas la tête. Le JSON ne contient pas de code Python à désérialiser; son hash est un contrôle local de cohérence, pas une signature d’auteur. Utiliser une source d’artefacts de confiance et les versions logicielles de référence.

## 5. Modifier les données

Créer une copie avant de modifier tickets.json. Conserver l’isolement train/adapt/validation/test et les group_id. Les mêmes données ne deviennent pas indépendantes parce que leur id change. Pour réentraîner dans un kernel déjà ouvert :

```python
from examples.week10.nlp import trained, specialized
specialized.cache_clear()
trained.cache_clear()
```

Ne pas choisir de nouveaux réglages après lecture des résultats test sans déclarer un nouveau protocole et un nouveau jeu réservé.

## 6. LoRA optionnel

Lire examples/week10/optional/README.md. Préparer un modèle BERT local, PyTorch, Transformers et PEFT dans un environnement séparé, puis verrouiller les versions réellement utilisées. Ce lab n’a pas été exécuté ici. L’adaptation obligatoire reste une tête linéaire sur TF-IDF figé.
