"""
Tests du lab Function Calling.

Exécution :
    python book/week02/day02/labs/test_function_calling_agent.py
"""

from function_calling_agent import (
    FakePlanner,
    ToolCall,
    ToolCallError,
    SupportAgent,
    build_registry,
)


def assert_raises(expected_code: str, func, *args, **kwargs) -> None:
    try:
        func(*args, **kwargs)
    except ToolCallError as exc:
        assert exc.code == expected_code, f"Code attendu={expected_code}, reçu={exc.code}"
        return

    raise AssertionError(f"Exception attendue: {expected_code}")


def test_valid_get_order_status() -> None:
    registry = build_registry()
    result = registry.dispatch(ToolCall("get_order_status", {"order_id": "ORD-1001"}))

    assert result["ok"] is True
    assert result["data"]["order_id"] == "ORD-1001"
    assert result["data"]["status"] == "shipped"


def test_unknown_tool_is_rejected() -> None:
    registry = build_registry()
    assert_raises("UNKNOWN_TOOL", registry.validate, ToolCall("delete_everything", {}))


def test_unexpected_argument_is_rejected() -> None:
    registry = build_registry()
    assert_raises(
        "UNEXPECTED_ARGUMENT",
        registry.validate,
        ToolCall("get_order_status", {"order_id": "ORD-1001", "debug": "true"}),
    )


def test_invalid_enum_is_rejected() -> None:
    registry = build_registry()
    assert_raises(
        "INVALID_ENUM_VALUE",
        registry.validate,
        ToolCall(
            "create_support_ticket",
            {
                "order_id": "ORD-1001",
                "issue": "Colis endommagé",
                "priority": "urgent",
            },
        ),
    )


def test_agent_returns_controlled_error() -> None:
    agent = SupportAgent(registry=build_registry(), planner=FakePlanner())
    response = agent.run("Déclenche un outil inconnu.")

    assert response["ok"] is False
    assert response["error"]["code"] == "UNKNOWN_TOOL"


def run_all_tests() -> None:
    test_valid_get_order_status()
    test_unknown_tool_is_rejected()
    test_unexpected_argument_is_rejected()
    test_invalid_enum_is_rejected()
    test_agent_returns_controlled_error()


if __name__ == "__main__":
    run_all_tests()
    print("Tous les tests du Jour 2 Semaine 2 sont passés.")
