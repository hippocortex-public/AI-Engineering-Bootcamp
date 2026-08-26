"""
Tests du lab S4 J3 — Tool Registry.

Exécution :
    python test_tool_registry.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def find_project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in [current.parent, *current.parents]:
        if (parent / "mini_framework").exists():
            return parent
    raise RuntimeError("Impossible de trouver la racine du projet.")


PROJECT_ROOT = find_project_root()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mini_framework.tool_registry import (  # noqa: E402
    ToolContext,
    ToolRegistry,
    ToolSchemaError,
    build_demo_registry,
    register_decorated,
    tool,
)


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_registry_lists_non_sensitive_tools_by_default() -> None:
    registry = build_demo_registry()
    names = {item["name"] for item in registry.list_tools()}
    assert_true("add_numbers" in names, "add_numbers doit être visible")
    assert_true("search_policy" in names, "search_policy doit être visible")
    assert_true("create_ticket" not in names, "outil sensible masqué par défaut")


def test_registry_can_include_sensitive_tools() -> None:
    registry = build_demo_registry()
    names = {item["name"] for item in registry.list_tools(include_sensitive=True)}
    assert_true("create_ticket" in names, "include_sensitive doit exposer create_ticket")


def test_successful_tool_call() -> None:
    registry = build_demo_registry()
    ctx = ToolContext(user_id="u1", session_id="s1")
    result = registry.call("add_numbers", {"a": 7, "b": 5}, ctx)
    assert_true(result.status == "completed", "appel attendu en completed")
    assert_true(result.output["sum"] == 12, "somme incorrecte")


def test_missing_required_argument_fails() -> None:
    registry = build_demo_registry()
    ctx = ToolContext(user_id="u1", session_id="s1")
    result = registry.call("add_numbers", {"a": 7}, ctx)
    assert_true(result.status == "failed", "argument manquant doit échouer")
    assert_true("Champs requis manquants" in result.error, "message d'erreur incorrect")


def test_wrong_argument_type_fails() -> None:
    registry = build_demo_registry()
    ctx = ToolContext(user_id="u1", session_id="s1")
    result = registry.call("add_numbers", {"a": "7", "b": 5}, ctx)
    assert_true(result.status == "failed", "type invalide doit échouer")
    assert_true("Type invalide" in result.error, "message de type attendu")


def test_enum_validation_fails() -> None:
    registry = build_demo_registry()
    ctx = ToolContext(
        user_id="u1",
        session_id="s1",
        scopes=frozenset({"ticket:write"}),
        approvals=frozenset({"create_ticket"}),
    )
    result = registry.call("create_ticket", {"title": "Bug", "priority": "urgent"}, ctx)
    assert_true(result.status == "failed", "enum invalide doit échouer")
    assert_true("Valeur invalide" in result.error, "message enum attendu")


def test_additional_properties_are_rejected() -> None:
    registry = build_demo_registry()
    ctx = ToolContext(user_id="u1", session_id="s1")
    result = registry.call("add_numbers", {"a": 1, "b": 2, "c": 3}, ctx)
    assert_true(result.status == "failed", "champ extra doit échouer")
    assert_true("Champs inattendus" in result.error, "message champ extra attendu")


def test_unknown_tool_returns_failed_result() -> None:
    registry = build_demo_registry()
    ctx = ToolContext(user_id="u1", session_id="s1")
    result = registry.call("unknown", {}, ctx)
    assert_true(result.status == "failed", "outil inconnu doit produire failed")
    assert_true("Outil inconnu" in result.error, "message outil inconnu attendu")


def test_disabled_tool_is_blocked() -> None:
    registry = build_demo_registry()
    ctx = ToolContext(user_id="u1", session_id="s1")
    result = registry.call("disabled_tool", {}, ctx)
    assert_true(result.status == "blocked", "outil désactivé doit être bloqué")
    assert_true("désactivé" in result.error, "message désactivé attendu")


def test_sensitive_tool_requires_approval() -> None:
    registry = build_demo_registry()
    ctx = ToolContext(user_id="u1", session_id="s1", scopes=frozenset({"ticket:write"}))
    result = registry.call("create_ticket", {"title": "Bug"}, ctx)
    assert_true(result.status == "blocked", "outil sensible doit être bloqué sans approbation")
    assert_true("Approbation humaine" in result.error, "message approbation attendu")


def test_required_scope_is_enforced() -> None:
    registry = build_demo_registry()
    ctx = ToolContext(user_id="u1", session_id="s1")
    result = registry.call("search_policy", {"query": "sla"}, ctx)
    assert_true(result.status == "blocked", "scope absent doit bloquer")
    assert_true("Scope requis" in result.error, "message scope attendu")


def test_trace_contains_validation_and_execution_steps() -> None:
    registry = build_demo_registry()
    ctx = ToolContext(user_id="u1", session_id="s1")
    result = registry.call("add_numbers", {"a": 1, "b": 2}, ctx)
    steps = [item["step"] for item in result.trace]
    assert_true("schema.validate" in steps, "trace de validation manquante")
    assert_true("tool.execute" in steps, "trace d'exécution manquante")
    assert_true("tool.completed" in steps, "trace de completion manquante")


def test_export_manifest_is_json_serializable() -> None:
    registry = build_demo_registry()
    payload = registry.export_manifest()
    serialized = json.dumps(payload, ensure_ascii=False)
    assert_true("handler" not in serialized, "le manifest ne doit pas exposer de callable")
    assert_true(payload["tool_count"] >= 3, "manifest incomplet")


def test_decorator_registers_function_tool() -> None:
    registry = ToolRegistry()

    @tool(description="Multiplie deux entiers.", tags=["math"])
    def multiply(a: int, b: int) -> dict:
        return {"product": a * b}

    register_decorated(registry, multiply)
    ctx = ToolContext(user_id="u1", session_id="s1")
    result = registry.call("multiply", {"a": 6, "b": 7}, ctx)
    assert_true(result.status == "completed", "tool décoré doit fonctionner")
    assert_true(result.output["product"] == 42, "produit incorrect")


def test_handler_exception_is_captured() -> None:
    registry = build_demo_registry()
    ctx = ToolContext(user_id="u1", session_id="s1")
    result = registry.call("fail_tool", {}, ctx)
    assert_true(result.status == "failed", "exception handler doit produire failed")
    assert_true("Erreur d'exécution" in result.error, "message exception attendu")


def run_all() -> None:
    tests = [
        test_registry_lists_non_sensitive_tools_by_default,
        test_registry_can_include_sensitive_tools,
        test_successful_tool_call,
        test_missing_required_argument_fails,
        test_wrong_argument_type_fails,
        test_enum_validation_fails,
        test_additional_properties_are_rejected,
        test_unknown_tool_returns_failed_result,
        test_disabled_tool_is_blocked,
        test_sensitive_tool_requires_approval,
        test_required_scope_is_enforced,
        test_trace_contains_validation_and_execution_steps,
        test_export_manifest_is_json_serializable,
        test_decorator_registers_function_tool,
        test_handler_exception_is_captured,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")


if __name__ == "__main__":
    run_all()
