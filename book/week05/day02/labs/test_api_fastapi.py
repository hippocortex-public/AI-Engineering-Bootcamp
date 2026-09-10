from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient

from ai_platform.api import APISettings, DeterministicSupportService, InMemoryRateLimiter, create_app


def assert_true(value, message):
    if not value:
        raise AssertionError(message)


def build_client(limit=5, require_api_key=True, max_message_chars=1200):
    settings = APISettings(
        title="Test AI API",
        version="0.2.0",
        require_api_key=require_api_key,
        api_key="test-key",
        rate_limit_per_session=limit,
        max_message_chars=max_message_chars,
    )
    service = DeterministicSupportService()
    app = create_app(settings=settings, service=service, limiter=InMemoryRateLimiter(limit))
    return TestClient(app), service


def auth_headers(request_id="req-test-001"):
    return {"X-API-Key": "test-key", "X-Request-ID": request_id}


def valid_payload(message="I have a billing issue with invoice 123"):
    return {
        "session_id": "session-123",
        "user_id": "user-123",
        "message": message,
        "metadata": {"channel": "test"},
    }


def test_health_is_public():
    client, _ = build_client()
    response = client.get("/healthz")
    assert_true(response.status_code == 200, response.text)
    assert_true(response.json()["status"] == "ok", "health endpoint should be ok")


def test_ready_is_public_and_reports_ready():
    client, _ = build_client()
    response = client.get("/readyz")
    assert_true(response.status_code == 200, response.text)
    assert_true(response.json()["status"] == "ready", "ready endpoint should be ready")


def test_chat_requires_api_key():
    client, _ = build_client()
    response = client.post("/v1/chat", json=valid_payload())
    assert_true(response.status_code == 401, response.text)
    assert_true("request_id" in response.json(), "error response should include request_id")


def test_chat_accepts_valid_request():
    client, _ = build_client()
    response = client.post("/v1/chat", headers=auth_headers(), json=valid_payload())
    body = response.json()
    assert_true(response.status_code == 200, response.text)
    assert_true(body["intent"] == "billing", body)
    assert_true(body["request_id"] == "req-test-001", body)
    assert_true(response.headers["X-Request-ID"] == "req-test-001", "request id should be echoed")


def test_validation_rejects_unknown_fields():
    client, _ = build_client()
    payload = valid_payload()
    payload["unexpected"] = True
    response = client.post("/v1/chat", headers=auth_headers(), json=payload)
    assert_true(response.status_code == 422, response.text)


def test_validation_rejects_unsafe_identifier():
    client, _ = build_client()
    payload = valid_payload()
    payload["session_id"] = "bad/session"
    response = client.post("/v1/chat", headers=auth_headers(), json=payload)
    assert_true(response.status_code == 422, response.text)


def test_configured_message_length_is_enforced():
    client, _ = build_client(max_message_chars=10)
    response = client.post("/v1/chat", headers=auth_headers(), json=valid_payload("this message is too long"))
    assert_true(response.status_code == 413, response.text)


def test_rate_limit_is_scoped_by_session():
    client, _ = build_client(limit=1)
    first = client.post("/v1/chat", headers=auth_headers("req-1"), json=valid_payload("billing question"))
    second = client.post("/v1/chat", headers=auth_headers("req-2"), json=valid_payload("another billing question"))
    assert_true(first.status_code == 200, first.text)
    assert_true(second.status_code == 429, second.text)
    assert_true(second.headers["X-RateLimit-Remaining"] == "0", "remaining rate limit should be reported")


def test_session_transcript_is_available_after_turn():
    client, _ = build_client()
    client.post("/v1/chat", headers=auth_headers("req-session"), json=valid_payload("technical error timeout"))
    response = client.get("/v1/sessions/session-123", headers=auth_headers("req-read"))
    body = response.json()
    assert_true(response.status_code == 200, response.text)
    assert_true(len(body["turns"]) == 1, body)
    assert_true(body["turns"][0]["intent"] == "technical", body)


def test_missing_session_returns_404():
    client, _ = build_client()
    response = client.get("/v1/sessions/missing-session", headers=auth_headers())
    assert_true(response.status_code == 404, response.text)


def test_pii_is_redacted_in_transcript():
    client, _ = build_client()
    client.post(
        "/v1/chat",
        headers=auth_headers("req-pii"),
        json=valid_payload("My email is alice@example.com and I have a billing issue"),
    )
    response = client.get("/v1/sessions/session-123", headers=auth_headers("req-read-pii"))
    body = response.json()
    assert_true("[redacted_email]" in body["turns"][0]["message"], body)
    assert_true("alice@example.com" not in body["turns"][0]["message"], body)


def test_sensitive_action_requires_review():
    client, _ = build_client()
    response = client.post(
        "/v1/chat",
        headers=auth_headers("req-sensitive"),
        json=valid_payload("Please delete account immediately"),
    )
    body = response.json()
    assert_true(response.status_code == 200, response.text)
    assert_true(body["safety_status"] == "needs_review", body)


def test_openapi_contains_ai_routes():
    client, _ = build_client()
    response = client.get("/openapi.json")
    paths = response.json()["paths"]
    assert_true("/v1/chat" in paths, "OpenAPI should expose chat route")
    assert_true("/v1/sessions/{session_id}" in paths, "OpenAPI should expose session route")


def test_api_can_run_without_api_key_for_local_demo():
    client, _ = build_client(require_api_key=False)
    response = client.post("/v1/chat", json=valid_payload("general question"))
    assert_true(response.status_code == 200, response.text)


def test_public_package_exports_day1_and_day2_symbols():
    from ai_platform import (  # noqa: E402
        APISettings,
        ArchitectureBlueprint,
        ChatRequest,
        DeterministicSupportService,
        create_app,
        build_support_ai_blueprint,
    )

    assert_true(APISettings is not None, "APISettings should be exported")
    assert_true(ChatRequest is not None, "ChatRequest should be exported")
    assert_true(DeterministicSupportService is not None, "DeterministicSupportService should be exported")
    assert_true(create_app is not None, "create_app should be exported")
    assert_true(ArchitectureBlueprint is not None, "day 1 ArchitectureBlueprint should remain exported")
    assert_true(build_support_ai_blueprint is not None, "day 1 factory should remain exported")


if __name__ == "__main__":
    tests = [
        test_health_is_public,
        test_ready_is_public_and_reports_ready,
        test_chat_requires_api_key,
        test_chat_accepts_valid_request,
        test_validation_rejects_unknown_fields,
        test_validation_rejects_unsafe_identifier,
        test_configured_message_length_is_enforced,
        test_rate_limit_is_scoped_by_session,
        test_session_transcript_is_available_after_turn,
        test_missing_session_returns_404,
        test_pii_is_redacted_in_transcript,
        test_sensitive_action_requires_review,
        test_openapi_contains_ai_routes,
        test_api_can_run_without_api_key_for_local_demo,
        test_public_package_exports_day1_and_day2_symbols,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
