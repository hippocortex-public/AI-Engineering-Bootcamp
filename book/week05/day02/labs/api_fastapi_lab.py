"""
Lab for Week 5 Day 2 — API FastAPI.

Run:
    python book/week05/day02/labs/api_fastapi_lab.py
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient

from ai_platform.api import APISettings, DeterministicSupportService, InMemoryRateLimiter, create_app


def build_demo_client() -> TestClient:
    settings = APISettings(
        title="Bootcamp Support API",
        version="0.2.0",
        api_key="local-dev-key",
        rate_limit_per_session=3,
        max_message_chars=500,
    )
    app = create_app(
        settings=settings,
        service=DeterministicSupportService(),
        limiter=InMemoryRateLimiter(settings.rate_limit_per_session),
    )
    return TestClient(app)


def run_demo() -> None:
    client = build_demo_client()

    health = client.get("/healthz")
    print("health:", health.json())

    response = client.post(
        "/v1/chat",
        headers={"X-API-Key": "local-dev-key", "X-Request-ID": "lab-request-001"},
        json={
            "session_id": "session-001",
            "user_id": "user-001",
            "message": "I have a billing issue with invoice INV-42",
            "metadata": {"channel": "web"},
        },
    )
    print("chat:", response.json())
    print("x-request-id:", response.headers["X-Request-ID"])

    transcript = client.get(
        "/v1/sessions/session-001",
        headers={"X-API-Key": "local-dev-key"},
    )
    print("transcript:", transcript.json())


if __name__ == "__main__":
    run_demo()
