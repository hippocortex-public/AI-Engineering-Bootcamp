# Démarrage et démonstration — Semaine 7

Toutes les commandes ci-dessous supposent que les répertoires du paquet ont été copiés dans la racine du dépôt. Python 3.12 est recommandé. Aucune dépendance pip n’est nécessaire pour le moteur et les tests.

## 1. Parcours Python immédiat

```bash
python3 -m examples.week07.demo 7
python3 -m unittest discover -s tests/week07 -v
python3 book/week07/day01/labs/run.py
python3 scripts/generate_week07_notebooks.py
```

La démo J7 doit retourner les compteurs `published:1`, `rejected:1`, `expired:1` et `publication_count:1`. Chaque lab J1 à J7 exécute un scénario spécifique. Les notebooks élève sont sous `notebooks/week07`; les notebooks enseignant sous `notebooks/week07/teacher`. Les fragments autonomes ne dépendent pas de Jupyter; un éditeur compatible suffit pour les lire. Pour les cellules enseignant qui importent le moteur, ouvrir depuis l’arbre du dépôt.

## 2. Préparer les secrets locaux

Créer un fichier local avec des valeurs distinctes, sans le commiter :

```bash
python3 - <<'PY'
from pathlib import Path
import secrets
path = Path('examples/week07/.env')
if path.exists():
    raise SystemExit('Le fichier existe déjà; conserver ses valeurs')
path.write_text('\n'.join(f'{key}={secrets.token_hex(32)}' for key in
                         ['SERVICE_TOKEN','REVIEW_TOKEN','N8N_ENCRYPTION_KEY'])+'\n')
path.chmod(0o600)
PY
```

Le fichier est exclu du Git et du contexte de construction Docker. Conserver la clé n8n si vous conservez son volume; la changer sans migration peut rendre les credentials stockés illisibles.

## 3. Backend HTTP sans Docker

Charger votre propre fichier de secrets dans le shell puis démarrer :

```bash
set -a
. examples/week07/.env
set +a
python3 -m examples.week07.server
```

Dans un deuxième terminal, depuis la même racine :

```bash
set -a
. examples/week07/.env
set +a
python3 -m examples.week07.smoke_http
```

Le serveur écoute par défaut sur 127.0.0.1:8080 et utilise `workflow.sqlite` dans le répertoire courant. Pour éviter de créer cette base à la racine du dépôt, définir `WORKFLOW_DB=examples/week07/workflow.sqlite` avant le démarrage. La base contient du texte métier : utiliser uniquement les événements fictifs du lab et définir une politique de rétention avant tout usage réel.

## 4. n8n et backend sous Docker Compose

```bash
cd examples/week07
set -a
. ./.env
set +a
 docker compose config
 docker compose up -d --build
 docker compose ps
```

Ouvrir http://127.0.0.1:5678 et créer le compte propriétaire local demandé par n8n. Image ciblée : `docker.n8n.io/n8nio/n8n:2.42.7`, version relevée dans la documentation officielle consultée. L’image est épinglée par tag, pas par digest. Le démarrage de cette image n’a pas été exécuté lors de la génération de ce paquet. Aucun composant n8n Assistant ou sandbox privilégié n’est nécessaire pour ces trois workflows.

L’installation du lab utilise SQLite et un volume persistant pour chaque service. Les deux ports publiés sont liés à 127.0.0.1. `N8N_SECURE_COOKIE=false` s’applique uniquement à ce test HTTP local. Avant un usage partagé, utiliser TLS et revoir l’authentification.

## 5. Importer et configurer les exports

Importer successivement `workflows/01_ingress.json`, `02_worker.json` et `03_decision.json` depuis le menu d’import de l’éditeur. Ils sont désactivés par défaut. Les credentials doivent être configurés après import; aucun export ne contient un identifiant ou une valeur de credential.

Créer deux credentials **Header Auth** avec nom d’en-tête `Authorization` :

| Credential local | Valeur | Affectation |
|---|---|---|
| S7 Service | `Bearer <SERVICE_TOKEN>` | Webhook Ingress, HTTP Persist event, HTTP Tick |
| S7 Review | `Bearer <REVIEW_TOKEN>` | Webhook Review, HTTP Decide |

Les mêmes tokens sont réutilisés pour les deux frontières locales du lab. Cette simplification ne convient pas à une installation multi-utilisateur; séparer identités et audiences dans une architecture réelle. Sélectionner le credential dans chaque nœud concerné, puis sauvegarder.

Dans HTTP Request, vérifier que la réponse inclut le status code et les headers, utilise JSON, et accepte les réponses HTTP non-2xx pour les propager. `Respond` utilise le `statusCode` du backend et son `body`. Sans ce réglage, un conflit métier 409 peut devenir une erreur technique générique de n8n.

Le workflow worker possède deux déclencheurs alternatifs : Manual pour un test dans l’éditeur et Schedule toutes les 10 secondes. Publier ou activer les trois workflows selon l’interface de la version installée. Copier les URLs de production affichées. Les chemins attendus sont `/webhook/week07-request` et `/webhook/week07-decision`; ne pas utiliser `/webhook-test` pour le script ci-dessous.

## 6. Vérification réelle du parcours n8n

Revenir à la racine du dépôt, avec les deux tokens exportés :

```bash
python3 -m examples.week07.smoke_http --n8n
```

Le script passe par le webhook de réception, attend jusqu’à 30 secondes que le scheduler n8n prépare le brouillon, puis passe par le webhook de décision. Il vérifie l’acceptation, le doublon, la collision, le rôle, la répétition d’approbation et la décision contradictoire. Il crée uniquement une publication dans la base locale. Il utilise un event_id nouveau à chaque exécution.

Si le script échoue, examiner l’exécution n8n et distinguer credential manquant, URL inactive, DNS Compose, body JSON et propagation du status code. Les fichiers JSON ont été contrôlés statiquement; l’import réel reste une étape nécessaire pour valider leur compatibilité avec votre installation.

## 7. Manipulations HTTP pour la relecture

Envoyer `assets/event.json` du jour au POST /events avec Authorization Bearer et SERVICE_TOKEN. Appeler POST /tick avec `{}`. Lire GET /jobs/{event_id}. Une décision utilise le token REVIEW_TOKEN et ce corps :

```json
{"decision":"approve","proposal_hash":"empreinte retournée par GET /jobs"}
```

L’identité ne vient pas d’un champ fourni par le client : le serveur associe le token de revue à `reviewer-demo`. Pour un refus, remplacer approve par reject. Une décision après expires_at retourne 409. Dans le moteur, l’horloge injectable permet de reproduire cette situation rapidement; dans le serveur réel, le TTL est d’une heure.

## 8. Arrêt et conservation

`docker compose down` arrête la stack et conserve les volumes. Ne pas utiliser `down -v` si vous souhaitez conserver jobs, credentials et historique. Les notebooks se régénèrent depuis les fichiers Markdown; ne pas éditer uniquement les notebooks.
