import logging

import pytest
import redis

from conftest import ALPHA_KEY, BETA_KEY, OPS_KEY


def headers(key=ALPHA_KEY):
    return {"X-API-Key": key}


def test_liveness_is_independent_of_database(client, repository):
    repository.available = False
    assert client.get("/health/live").status_code == 200
    assert client.get("/health/ready").status_code == 503


def test_readiness_requires_redis(client, backend, monkeypatch):
    monkeypatch.setattr(backend, "ready", lambda: False)
    assert client.get("/health/ready").status_code == 503


def test_readiness_when_all_dependencies_ready(client):
    assert client.get("/health/ready").status_code == 200


@pytest.mark.parametrize("key", [None, "invalid", "z" * 40])
def test_chat_requires_valid_identity(client, key):
    response = client.post("/chat", json={"message": "Bonjour"}, headers=headers(key) if key else {})
    assert response.status_code == 401


def test_alpha_cannot_read_beta_by_document_or_chat(client):
    assert client.get("/documents/beta-guide", headers=headers()).status_code == 404
    response = client.post("/chat", json={"message": "Résume", "document_id": "beta-guide"}, headers=headers())
    assert response.status_code == 404
    assert "BETA_PRIVATE" not in response.text


def test_cache_hit_and_revocation_are_checked(client, repository):
    payload = {"message": "Résume", "document_id": "alpha-guide"}
    first = client.post("/chat", json=payload, headers=headers())
    second = client.post("/chat", json=payload, headers=headers())
    assert first.status_code == second.status_code == 200
    assert first.json()["cached"] is False and second.json()["cached"] is True
    repository.visible = False
    assert client.post("/chat", json=payload, headers=headers()).status_code == 404


def test_changed_document_changes_cache_key(client, repository):
    from deployment_ai_service.storage import Document
    payload = {"message": "Résume", "document_id": "alpha-guide"}
    client.post("/chat", json=payload, headers=headers())
    repository.documents[("alpha", "alpha-guide")] = Document("alpha-guide", "NEW_CONTENT")
    response = client.post("/chat", json=payload, headers=headers())
    assert response.json()["cached"] is False
    assert "NEW_CONTENT" in response.json()["answer"]


def test_metrics_require_dedicated_scope(client):
    assert client.get("/metrics").status_code == 401
    assert client.get("/metrics", headers=headers()).status_code == 403
    client.post("/chat", json={"message": "Bonjour"}, headers=headers())
    response = client.get("/metrics", headers=headers(OPS_KEY))
    assert response.status_code == 200
    assert "text/plain" in response.headers["Content-Type"]
    assert "ai_http_requests_total" in response.text
    assert ALPHA_KEY not in response.text and "alice" not in response.text


@pytest.mark.parametrize("payload", [{"message": "x", "tenant": "beta"}, {"message": " "}, {"message": "x" * 2001}])
def test_payload_validation(client, payload):
    assert client.post("/chat", json=payload, headers=headers()).status_code == 422


def test_redis_failure_fails_closed_without_secret(client, backend, monkeypatch):
    def fail(*args):
        raise redis.ConnectionError("redis://SECRET_PASSWORD")
    monkeypatch.setattr(backend.client, "eval", fail)
    response = client.post("/chat", json={"message": "Bonjour"}, headers=headers())
    assert response.status_code == 503
    assert "SECRET_PASSWORD" not in response.text


def test_audit_does_not_expose_prompt_or_key(client, caplog):
    with caplog.at_level(logging.INFO, logger="deployment_ai_service.audit"):
        response = client.post("/chat", json={"message": "PRIVATE_PROMPT"}, headers=headers())
    assert response.status_code == 200
    assert "PRIVATE_PROMPT" not in caplog.text and ALPHA_KEY not in caplog.text
    assert response.headers["X-Request-ID"] in caplog.text
