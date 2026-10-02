# Lab — Déployer API IA, PostgreSQL et Redis

## Prérequis

Python 3.11+ pour les tests locaux, Docker Engine ou Docker Desktop avec Compose V2
supportant `up --wait`. Le lab fonctionne en conteneur Python 3.12 Linux. Port 8000
libre sur localhost. Les images sont multi-architecture ; vérifier votre plateforme.

Depuis `book/week05/day07/labs/` :

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Sous PowerShell : `.venv\Scripts\Activate.ps1`. Les étapes Docker sont identiques,
mais l'affectation temporaire des variables doit être adaptée à PowerShell.

## 1. Configurer une fois

```bash
python configure_demo.py
docker compose config -q
```

Ne pas ajouter `secrets/` à Git, ne pas afficher ses fichiers et ne pas activer le
tracing shell. Le script refuse de remplacer un dossier déjà présent. Les mots de
passe doivent rester cohérents avec les volumes PostgreSQL et Redis existants.

## 2. Construire et démarrer

```bash
docker compose build api
docker compose up -d --wait --wait-timeout 120
docker compose ps
python smoke_test.py
```

Les deux premières commandes construisent l'image puis démarrent les trois services.
`smoke_test.py` lit les clés sans les afficher et exécute neuf contrôles. Il consomme
quatre appels du quota d'Alice ; plusieurs exécutions rapprochées peuvent donner 429.
Attendre l'expiration de la fenêtre avant une nouvelle série si nécessaire.

## 3. Observer

```bash
curl --fail http://127.0.0.1:8000/health/live
curl --fail http://127.0.0.1:8000/health/ready
docker compose logs --tail=50 api
```

Pour consulter les métriques, utiliser la clé de l'identité operator via un client
qui ne l'imprime pas. Le smoke test vérifie déjà ce point. Aucun serveur Prometheus
ou Grafana n'est démarré par ce lab.

## 4. Examiner une panne de dépendance

```bash
docker compose stop redis
curl http://127.0.0.1:8000/health/ready
curl --fail http://127.0.0.1:8000/health/live
docker compose start redis
docker compose up -d --wait --wait-timeout 120
```

La readiness retourne 503 pendant la panne ; la liveness continue de répondre.
Une requête de chat authentifiée échoue également en 503, car Redis porte le quota.
Cette expérimentation modifie votre stack locale du lab ; ne pas l'exécuter sur un
service partagé.

## 5. Livrer une deuxième image

Après une modification applicative contrôlée et ses tests :

```bash
APP_IMAGE=bootcamp-ai:release-002 APP_RELEASE=release-002 docker compose build api
APP_IMAGE=bootcamp-ai:release-002 APP_RELEASE=release-002 docker compose up -d --no-deps --no-build --wait --wait-timeout 120 api
python smoke_test.py
```

Conserver l'image précédente et l'association commit/image. Un tag de lab n'est pas
un digest immuable ; ne pas déplacer ses tags durant l'exercice.

## 6. Rollback API

```bash
APP_IMAGE=bootcamp-ai:release-001 APP_RELEASE=release-001 docker compose up -d --no-deps --no-build --wait --wait-timeout 120 api
python smoke_test.py
```

Les dépendances doivent rester démarrées. Aucun volume n'est supprimé. Le rollback
suppose que le schéma est compatible avec release-001. Si les smoke tests dépassent
le quota après plusieurs tentatives, attendre l'échéance ; ne pas effacer les quotas
pour masquer un problème réel.

## 7. Arrêt sans perte des volumes

```bash
docker compose down
```

Éviter `down --volumes` pour conserver les données. Les scripts d'initialisation ne
se rejouent pas sur le volume existant. Ne pas régénérer des mots de passe arbitrairement.

## Validation sans Docker

Les tests utilisent un dépôt SQL simulé et fakeredis avec Lua. Ils exécutent le
script de quota, les permissions, le cache, les décisions de rollout et les contrôles
statiques des fichiers. Ils ne testent pas l'image, le bootstrap réel ou les montages
Docker. La stack doit encore être exécutée sur une machine disposant de Docker.

## Notebooks

Installer `requirements-dev.txt` dans le kernel choisi. Depuis la racine :

```bash
python book/week05/day07/labs/generate_notebooks.py
```

Les cellules utilisent des doubles de dépendances et ne lancent pas de conteneurs.
Les commandes Docker restent dans les sources Markdown. Le modèle reste simulé.
