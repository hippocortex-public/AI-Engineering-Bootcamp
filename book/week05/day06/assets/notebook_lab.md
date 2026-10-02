# Atelier exécutable du notebook

Ces cellules utilisent le lab fourni et n'exigent ni fichier de clés ni réseau.
Les clés sont générées dans la mémoire du kernel et ne sont pas affichées.
Installer les dépendances du lab dans le kernel Python sélectionné avant de lancer.

## 1. Retrouver le dépôt et créer les identités

```python
from pathlib import Path
import sys
import secrets

candidates = [Path.cwd(), *Path.cwd().parents]
root = next((p for p in candidates if (p / "book/week05/day06/labs").is_dir()), None)
if root is None:
    raise RuntimeError("Ouvrir le notebook depuis ai-engineering-bootcamp ou ses sous-dossiers.")
lab = root / "book/week05/day06/labs"
if str(lab) not in sys.path:
    sys.path.insert(0, str(lab))

from fastapi.testclient import TestClient
from security_ai_service.app import create_app
from security_ai_service.auth import Credential, IdentityStore, Principal
from security_ai_service.quota import FixedWindowLimiter, QuotaExceeded

alice = Principal("alice", "alpha", frozenset({"chat:write", "documents:read", "tools:read"}))
key = secrets.token_urlsafe(32)
identities = IdentityStore([Credential(key, alice)])
client = TestClient(create_app(identities=identities, limiter=FixedWindowLimiter(100)))
headers = {"X-API-Key": key}
print("Principal prêt :", alice.subject, alice.tenant)
```

## 2. Observer les frontières d'accès

```python
cases = [
    ("Sans identité", client.post("/chat", json={"message": "Bonjour"}), 401),
    ("Lecture alpha", client.get("/documents/alpha-guide", headers=headers), 200),
    ("Lecture beta", client.get("/documents/beta-guide", headers=headers), 404),
    ("Outil interdit", client.post("/tools/invoke", json={"name": "shell", "arguments": {}}, headers=headers), 403),
    ("Tenant imposé", client.post("/chat", json={"message": "Bonjour", "tenant": "beta"}, headers=headers), 422),
    ("Chat autorisé", client.post("/chat", json={"message": "Résume", "document_id": "alpha-guide"}, headers=headers), 200),
]
for name, response, expected in cases:
    assert response.status_code == expected, (name, response.status_code)
    print(name, ":", response.status_code)
```

## 3. Vérifier le renouvellement du quota sans attendre

```python
clock = [0.0]
quota = FixedWindowLimiter(2, 60, lambda: clock[0])
quota.consume(alice)
quota.consume(alice)
try:
    quota.consume(alice)
except QuotaExceeded as error:
    assert error.retry_after == 60
    print("Quota atteint ; Retry-After :", error.retry_after)
else:
    raise AssertionError("Le troisième appel doit être refusé")
clock[0] = 60.0
quota.consume(alice)
print("Fenêtre suivante : appel autorisé")
```

## 4. Inspecter un audit sans conserver le prompt

```python
import io
import json
import logging

stream = io.StringIO()
logger = logging.getLogger("security_ai_service.audit")
handler = logging.StreamHandler(stream)
previous_level = logger.level
logger.addHandler(handler)
logger.setLevel(logging.INFO)
try:
    response = client.post("/chat", json={"message": "PRIVATE_NOTE"}, headers=headers)
finally:
    logger.removeHandler(handler)
    logger.setLevel(previous_level)
assert response.status_code == 200
assert "PRIVATE_NOTE" not in stream.getvalue()
assert key not in stream.getvalue()
audit = json.loads(stream.getvalue().strip())
assert audit["request_id"] == response.headers["X-Request-ID"]
print("Audit contrôlé :", audit["event"], audit["route"], audit["status_code"])
client.close()
```

## 5. Travail personnel

Résoudre les exercices sans consulter les corrections. Pour les extensions, modifier
une copie des modules et écrire les tests d'accès correspondants. Les résultats
ci-dessus prouvent des contrôles backend ; ils ne certifient pas un vrai modèle.
