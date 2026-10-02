# Atelier exécutable — Déploiement sans moteur Docker

Les cellules utilisent les dépendances de `labs/requirements-dev.txt`. Elles
exécutent les contrats API et le Lua Redis en mémoire, sans preuve de déploiement
ou de connexion à PostgreSQL réel. Les commandes de la stack sont dans `labs/README.md`.

## 1. Retrouver le lab et préparer des dépendances de test

```python
from pathlib import Path
import sys
import secrets

root = next((p for p in [Path.cwd(), *Path.cwd().parents]
    if (p / "book/week05/day07/labs").is_dir()), None)
if root is None:
    raise RuntimeError("Ouvrir le notebook depuis ai-engineering-bootcamp ou ses sous-dossiers.")
lab = root / "book/week05/day07/labs"
if str(lab) not in sys.path:
    sys.path.insert(0, str(lab))

import fakeredis
from fastapi.testclient import TestClient
from deployment_ai_service.app import create_app
from deployment_ai_service.auth import Credential, IdentityStore, Principal
from deployment_ai_service.storage import Document, DocumentNotFound, RedisBackend, RateLimited, require_scope

class DemoRepository:
    def __init__(self):
        self.available = True
    def ready(self):
        return self.available
    def get(self, principal, document_id):
        require_scope(principal, "documents:read")
        if principal.tenant != "alpha" or document_id != "alpha-guide":
            raise DocumentNotFound
        return Document("alpha-guide", "Guide privé alpha")

alice = Principal("alice", "alpha", frozenset({"chat:write", "documents:read"}))
operator = Principal("operator", "platform", frozenset({"metrics:read"}))
key, ops_key = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
identities = IdentityStore([Credential(key, alice), Credential(ops_key, operator)])
repository = DemoRepository()
redis_client = fakeredis.FakeRedis(decode_responses=True)
backend = RedisBackend(redis_client, limit=100)
client = TestClient(create_app(identities, repository, backend))
headers, ops_headers = {"X-API-Key": key}, {"X-API-Key": ops_key}
print("Dépendances de test prêtes ; aucun secret affiché")
```

## 2. Distinguer santé du processus et readiness

```python
assert client.get("/health/live").status_code == 200
assert client.get("/health/ready").status_code == 200
repository.available = False
assert client.get("/health/live").status_code == 200
assert client.get("/health/ready").status_code == 503
repository.available = True
print("Liveness indépendante de la disponibilité SQL")
```

## 3. Vérifier cache, isolation et métriques

```python
payload = {"message": "Résume", "document_id": "alpha-guide"}
first = client.post("/chat", json=payload, headers=headers)
second = client.post("/chat", json=payload, headers=headers)
assert first.status_code == second.status_code == 200
assert first.json()["cached"] is False
assert second.json()["cached"] is True
assert client.get("/documents/beta-guide", headers=headers).status_code == 404
assert client.get("/metrics", headers=headers).status_code == 403
metrics = client.get("/metrics", headers=ops_headers)
assert metrics.status_code == 200 and "ai_cache_hits_total" in metrics.text
assert key not in metrics.text
print("Cache autorisé, beta refusé et métriques protégées")
```

## 4. Démontrer un quota commun à deux instances

```python
shared = fakeredis.FakeRedis(decode_responses=True)
instance_one = RedisBackend(shared, limit=1)
instance_two = RedisBackend(shared, limit=1)
instance_one.consume(alice)
try:
    instance_two.consume(alice)
except RateLimited as error:
    assert 1 <= error.retry_after <= 60
    print("Deuxième instance limitée par le même quota")
else:
    raise AssertionError("Le quota n'est pas partagé")
client.close()
```

## 5. Passage à la stack réelle

Sur une machine disposant de Docker, suivre le README du lab, puis comparer :
sondes, lecture SQL réelle, données conservées après redémarrage, quotas partagés et
smoke tests. Les résultats ci-dessus ne prouvent ni l'image, ni les montages, ni
le bootstrap PostgreSQL. Résoudre les exercices avant de consulter leurs corrigés.
