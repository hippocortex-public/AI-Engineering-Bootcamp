# Lab — API IA sécurisée

## Ce que vous exécutez

Un service FastAPI avec un registre d'identités privé, des documents alpha/beta,
un outil autorisé, un quota par identité et un audit JSON. Aucune clé LLM, base ou
connexion cloud n'est nécessaire. Python 3.11+ ; versions directes fixées.

## Installation

Depuis `book/week05/day06/labs/` :

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

Sous PowerShell, activer avec `.venv\Scripts\Activate.ps1`.

## Configuration locale

Le script suivant génère des clés aléatoires et un fichier privé dans ce dossier :

```bash
python configure_demo.py
export SECURITY_IDENTITIES_JSON="$(cat .demo-identities.json)"
python -m uvicorn security_ai_service.app:create_app --factory --host 127.0.0.1 --port 8000
```

Ne pas activer `set -x`, ne pas versionner `.demo-identities.json` et ne pas placer
cette variable dans le frontend. L'application refuse de démarrer sans configuration.
Le script refuse d'écraser un fichier existant. Pour une rotation de démonstration,
conserver la copie utile, puis supprimer explicitement l'ancien fichier avant une
nouvelle génération. Les identités sont lues au démarrage.

## Scénarios HTTP

Dans un second terminal, même environnement virtuel et même dossier :

```bash
python demo_client.py
```

Le client lit les clés locales sans les afficher et vérifie : santé publique,
401 anonyme, lecture autorisée alpha, refus de beta par route directe/chat/outil,
403 outil shell et refus d'un payload cherchant à imposer un tenant. Il utilise
moins de dix appels protégés pour Alice sur un serveur fraîchement démarré.
Si vous le relancez rapidement, des 429 sont attendus ; attendre la fin de la
fenêtre ou redémarrer le serveur de démonstration. Le client est un scénario manuel,
pas le remplacement des tests isolés.

## Quota

Dix appels protégés par fenêtre de soixante secondes, communs au chat, aux documents
et aux outils pour le même sujet/tenant. Les tentatives authentifiées valides en
scope comptent, même si leur accès documentaire échoue. Les payloads invalides
peuvent aussi consommer un quota car les dépendances sont évaluées avant le handler.
Les appels anonymes ne consomment pas le quota d'un sujet.

## Corrigé du challenge

La classe `BudgetLedger` dans `budget_solution.py` implémente réservations,
finalisations et annulations. Son jeu de tests fait partie du lab. Lire d'abord
`../challenge.md` avant de consulter ce code.

## Génération des notebooks

Depuis la racine du dépôt, avec `nbformat` installé dans un environnement d'édition :

```bash
python -m pip install nbformat==5.10.4
python book/week05/day06/labs/generate_notebooks.py
```

Le Markdown constitue la source de vérité. Modifier les fichiers du jour puis
régénérer ; ne pas maintenir des corrections uniquement dans le notebook.

## Limites

Modèle simulé, documents et quotas en mémoire, un processus. Pas de TLS dans ce
serveur localhost, de coffre-fort, de RLS, de cache ni d'agent MCP. La validation
à 2 000 caractères ne remplace pas une limite de corps au niveau du serveur d'entrée.
Les tests ne certifient pas la résistance d'un LLM réel aux injections.
