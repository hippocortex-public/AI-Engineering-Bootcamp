import fakeredis
import pytest
from fastapi.testclient import TestClient

from deployment_ai_service.app import create_app
from deployment_ai_service.auth import Credential, IdentityStore, Principal
from deployment_ai_service.storage import Document, DocumentNotFound, RedisBackend, require_scope

ALPHA_KEY = "a" * 40
BETA_KEY = "b" * 40
OPS_KEY = "o" * 40


class MemoryRepository:
    """Double de test ; la requête SQL du dépôt réel est testée séparément."""
    def __init__(self):
        self.available = True
        self.visible = True
        self.documents = {
            ("alpha", "alpha-guide"): Document("alpha-guide", "ALPHA_PRIVATE"),
            ("beta", "beta-guide"): Document("beta-guide", "BETA_PRIVATE"),
        }

    def ready(self):
        return self.available

    def get(self, principal, document_id):
        require_scope(principal, "documents:read")
        if not self.visible or (principal.tenant, document_id) not in self.documents:
            raise DocumentNotFound
        return self.documents[(principal.tenant, document_id)]


@pytest.fixture
def repository():
    return MemoryRepository()


@pytest.fixture
def redis_client():
    return fakeredis.FakeRedis(decode_responses=True)


@pytest.fixture
def identities():
    return IdentityStore([
        Credential(ALPHA_KEY, Principal("alice", "alpha", frozenset({"chat:write", "documents:read"}))),
        Credential(BETA_KEY, Principal("bob", "beta", frozenset({"chat:write", "documents:read"}))),
        Credential(OPS_KEY, Principal("operator", "platform", frozenset({"metrics:read"}))),
    ])


@pytest.fixture
def backend(redis_client):
    return RedisBackend(redis_client, limit=100)


@pytest.fixture
def client(identities, repository, backend):
    with TestClient(create_app(identities, repository, backend), raise_server_exceptions=False) as client:
        yield client
