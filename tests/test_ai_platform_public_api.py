from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def assert_true(value, message):
    if not value:
        raise AssertionError(message)


def test_week05_public_api_is_cumulative():
    from ai_platform import (  # noqa: E402
        ArchitectureBlueprint,
        ProductionArchitectureValidator,
        APISettings,
        ChatRequest,
        ChatResponse,
        DeterministicSupportService,
        InMemoryRateLimiter,
        create_app,
    )

    assert_true(ArchitectureBlueprint is not None, "week 5 day 1 export missing")
    assert_true(ProductionArchitectureValidator is not None, "week 5 day 1 validator missing")
    assert_true(APISettings is not None, "week 5 day 2 settings missing")
    assert_true(ChatRequest is not None, "week 5 day 2 request model missing")
    assert_true(ChatResponse is not None, "week 5 day 2 response model missing")
    assert_true(DeterministicSupportService is not None, "week 5 day 2 service missing")
    assert_true(InMemoryRateLimiter is not None, "week 5 day 2 limiter missing")
    assert_true(create_app is not None, "week 5 day 2 app factory missing")


def test_app_factory_builds_fastapi_app():
    from ai_platform import APISettings, create_app  # noqa: E402

    app = create_app(APISettings(require_api_key=False))
    paths = set(app.openapi()["paths"].keys())
    assert_true("/healthz" in paths, "health route missing")
    assert_true("/readyz" in paths, "ready route missing")
    assert_true("/v1/chat" in paths, "chat route missing")


def test_service_classifies_intent_deterministically():
    from ai_platform import ChatRequest, DeterministicSupportService  # noqa: E402

    service = DeterministicSupportService()
    response = service.answer(
        ChatRequest(session_id="s-001", user_id="u-001", message="timeout error on endpoint"),
        request_id="req-001",
    )
    assert_true(response.intent == "technical", response.model_dump())


if __name__ == "__main__":
    tests = [
        test_week05_public_api_is_cumulative,
        test_app_factory_builds_fastapi_app,
        test_service_classifies_intent_deterministically,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
