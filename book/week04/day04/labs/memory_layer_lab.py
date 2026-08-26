"""
Lab entrypoint for S4 J4 - Memory Layer.

Run:
    python memory_layer_lab.py
    python test_memory_layer.py
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from mini_framework.memory import MemoryQuery, MemoryStore


def build_demo_store() -> MemoryStore:
    """Build a deterministic store used by the README, notebook and tests."""

    store = MemoryStore()
    now = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)

    store.add(
        namespace="user:alice",
        owner_agent="planner",
        kind="preference",
        content="Alice préfère des réponses structurées avec étapes numérotées.",
        visibility="private",
        tags=["preference", "format"],
        importance=0.9,
        now=now,
    )
    store.add(
        namespace="user:alice",
        owner_agent="researcher",
        kind="fact",
        content="Le projet cible un assistant IA mono-agent puis multi-agent.",
        visibility="shared",
        tags=["project", "bootcamp"],
        importance=0.75,
        now=now,
    )
    store.add(
        namespace="user:bob",
        owner_agent="planner",
        kind="preference",
        content="Bob préfère des réponses très courtes.",
        visibility="private",
        tags=["preference"],
        importance=0.8,
        now=now,
    )
    return store


def build_context_memory_pack(store: MemoryStore, namespace: str, request: str) -> list[dict]:
    """Return memory records ready to inject into a prompt context."""

    results = store.retrieve(
        MemoryQuery(
            namespace=namespace,
            text=request,
            requester_agent="planner",
            allowed_visibility=("private", "shared"),
            limit=3,
        )
    )
    return [
        {
            "id": result.record.id,
            "kind": result.record.kind,
            "content": result.record.content,
            "score": result.score,
            "reasons": result.reasons,
        }
        for result in results
    ]


def main() -> None:
    store = build_demo_store()
    pack = build_context_memory_pack(store, "user:alice", "Préparer le projet bootcamp avec format structuré")
    for item in pack:
        print(f"- [{item['kind']}] score={item['score']}: {item['content']}")


if __name__ == "__main__":
    main()
