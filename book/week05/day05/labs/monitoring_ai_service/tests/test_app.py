from fastapi.testclient import TestClient

from monitoring_ai_service.app import app, metrics_store


def test_chat_records_metrics() -> None:
    metrics_store.reset()
    client = TestClient(app)

    response = client.post("/chat", json={"message": "Explique le monitoring IA."})

    assert response.status_code == 200
    payload = response.json()
    assert payload["request_id"].startswith("req_")
    assert payload["answer"]

    metrics = client.get("/metrics").json()
    assert metrics["request_count"] == 1
    assert metrics["total_tokens"] > 0


def test_empty_response_is_visible_in_metrics() -> None:
    metrics_store.reset()
    client = TestClient(app)

    response = client.post("/chat", json={"message": "empty"})
    assert response.status_code == 200

    metrics = client.get("/metrics").json()
    assert metrics["empty_response_count"] == 1


def test_request_id_is_correlated_without_logging_prompt(caplog) -> None:
    import logging
    with caplog.at_level(logging.INFO, logger="uvicorn.error"):
        response = TestClient(app).post("/chat", json={"message": "PRIVATE_PROMPT"})
    assert response.headers["x-request-id"] == response.json()["request_id"]
    assert response.json()["request_id"] in caplog.text
    assert "PRIVATE_PROMPT" not in caplog.text


def test_provider_failure_is_counted_and_does_not_expose_secret(monkeypatch) -> None:
    import importlib
    module = importlib.import_module("monitoring_ai_service.app")
    def fail(message):
        raise RuntimeError("PRIVATE_PROVIDER_SECRET")
    monkeypatch.setattr(module, "simulate_model_answer", fail)
    metrics_store.reset()
    response = TestClient(app).post("/chat", json={"message": "Bonjour"})
    assert response.status_code == 500
    assert "PRIVATE_PROVIDER_SECRET" not in response.text
    assert metrics_store.snapshot()["error_count"] == 1
