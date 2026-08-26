"""
Semaine 4 — Jour 3
Lab : Tool Registry

Ce script exécute le registre d'outils du mini-framework avec des cas simples.
Il n'utilise aucune dépendance externe ni clé API.

Depuis ce dossier :
    python tool_registry_lab.py

Depuis la racine :
    python book/week04/day03/labs/tool_registry_lab.py
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

from mini_framework.tool_registry import ToolContext, build_demo_registry  # noqa: E402


def main() -> None:
    registry = build_demo_registry()

    safe_context = ToolContext(
        user_id="learner_001",
        session_id="s4j3",
        scopes=frozenset({"policy:read"}),
    )

    print("=== Tools visibles par défaut ===")
    print(json.dumps(registry.list_tools(), indent=2, ensure_ascii=False))

    print("\n=== Appel add_numbers ===")
    print(json.dumps(
        registry.call("add_numbers", {"a": 10, "b": 32}, safe_context).to_dict(),
        indent=2,
        ensure_ascii=False,
    ))

    print("\n=== Appel search_policy ===")
    print(json.dumps(
        registry.call("search_policy", {"query": "security"}, safe_context).to_dict(),
        indent=2,
        ensure_ascii=False,
    ))

    print("\n=== Appel sensible sans approbation ===")
    print(json.dumps(
        registry.call("create_ticket", {"title": "Escalade production", "priority": "high"}, safe_context).to_dict(),
        indent=2,
        ensure_ascii=False,
    ))


if __name__ == "__main__":
    main()
