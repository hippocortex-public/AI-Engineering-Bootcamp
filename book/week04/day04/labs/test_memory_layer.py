from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
import sys
import unittest

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from mini_framework.memory import MemoryQuery, MemoryStore, redact_pii
from memory_layer_lab import build_context_memory_pack, build_demo_store


class MemoryLayerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)

    def test_add_and_retrieve_relevant_memory(self) -> None:
        store = MemoryStore()
        store.add(
            namespace="user:1",
            owner_agent="planner",
            kind="preference",
            content="L'utilisateur préfère les réponses en Markdown.",
            tags=["markdown", "preference"],
            importance=0.9,
            now=self.now,
        )

        results = store.retrieve(MemoryQuery(namespace="user:1", text="format markdown"))
        self.assertEqual(len(results), 1)
        self.assertIn("Markdown", results[0].record.content)
        self.assertGreater(results[0].score, 0.9)

    def test_namespace_isolation_prevents_cross_user_leakage(self) -> None:
        store = build_demo_store()
        alice_results = store.retrieve(MemoryQuery(namespace="user:alice", text="réponses courtes"))
        self.assertTrue(alice_results)
        self.assertTrue(all(record.record.namespace == "user:alice" for record in alice_results))
        self.assertFalse(any("Bob" in record.record.content for record in alice_results))

    def test_visibility_filter_controls_context_injection(self) -> None:
        store = MemoryStore()
        store.add(namespace="tenant", owner_agent="agent", kind="fact", content="Public fact", visibility="public", now=self.now)
        store.add(namespace="tenant", owner_agent="agent", kind="fact", content="Shared fact", visibility="shared", now=self.now)
        store.add(namespace="tenant", owner_agent="agent", kind="fact", content="Private fact", visibility="private", now=self.now)

        results = store.retrieve(
            MemoryQuery(namespace="tenant", text="fact", allowed_visibility=("public", "shared"))
        )

        contents = {result.record.content for result in results}
        self.assertEqual(contents, {"Public fact", "Shared fact"})

    def test_ttl_expired_records_are_excluded_by_default(self) -> None:
        store = MemoryStore()
        store.add(
            namespace="session",
            owner_agent="agent",
            kind="task_state",
            content="Temporary state",
            ttl_seconds=10,
            now=self.now,
        )

        later = self.now + timedelta(seconds=11)
        results = store.retrieve(MemoryQuery(namespace="session", text="Temporary", now=later))
        self.assertEqual(results, [])

        with_expired = store.retrieve(
            MemoryQuery(namespace="session", text="Temporary", now=later, include_expired=True)
        )
        self.assertEqual(len(with_expired), 1)

    def test_update_increments_version_and_audit_log(self) -> None:
        store = MemoryStore()
        record = store.add(namespace="n", owner_agent="a", kind="fact", content="v1", now=self.now)
        updated = store.update(record.id, content="v2", importance=0.8, now=self.now + timedelta(seconds=1))

        self.assertEqual(updated.version, 2)
        self.assertEqual(updated.content, "v2")
        self.assertEqual(updated.importance, 0.8)
        self.assertEqual([event["action"] for event in store.audit_log], ["add", "update"])

    def test_delete_removes_one_record(self) -> None:
        store = MemoryStore()
        record = store.add(namespace="n", owner_agent="a", kind="fact", content="delete me", now=self.now)
        store.delete(record.id, now=self.now)

        self.assertEqual(store.list_records(namespace="n"), [])
        self.assertEqual(store.audit_log[-1]["action"], "delete")

    def test_forget_namespace_deletes_only_target_namespace(self) -> None:
        store = MemoryStore()
        store.add(namespace="user:a", owner_agent="a", kind="fact", content="A1", now=self.now)
        store.add(namespace="user:a", owner_agent="a", kind="fact", content="A2", now=self.now)
        store.add(namespace="user:b", owner_agent="a", kind="fact", content="B1", now=self.now)

        count = store.forget_namespace("user:a", now=self.now)

        self.assertEqual(count, 2)
        self.assertEqual(len(store.list_records(namespace="user:a")), 0)
        self.assertEqual(len(store.list_records(namespace="user:b")), 1)

    def test_redact_pii_on_write(self) -> None:
        store = MemoryStore()
        record = store.add(
            namespace="n",
            owner_agent="a",
            kind="fact",
            content="Contact: jane@example.com +33 6 12 34 56 78",
            now=self.now,
        )

        self.assertIn("[REDACTED_EMAIL]", record.content)
        self.assertIn("[REDACTED_PHONE]", record.content)
        self.assertNotIn("jane@example.com", record.content)

    def test_promote_event_keeps_only_reusable_information(self) -> None:
        store = MemoryStore()
        ignored = store.promote_event(
            namespace="user:1",
            owner_agent="agent",
            event_text="Bonjour",
            event_type="smalltalk",
            now=self.now,
        )
        promoted = store.promote_event(
            namespace="user:1",
            owner_agent="agent",
            event_text="I prefer bullet points for architecture reviews.",
            event_type="user_feedback",
            now=self.now,
        )

        self.assertIsNone(ignored)
        self.assertIsNotNone(promoted)
        self.assertEqual(promoted.kind, "preference")
        self.assertIn("feedback", promoted.tags)

    def test_snapshot_roundtrip_preserves_records(self) -> None:
        store = build_demo_store()
        snapshot = store.snapshot()
        restored = MemoryStore.from_snapshot(json.loads(json.dumps(snapshot)))

        self.assertEqual(len(restored.list_records(include_expired=True)), 3)
        self.assertEqual(len(restored.audit_log), 3)

    def test_retrieval_prioritizes_query_match_and_importance(self) -> None:
        store = MemoryStore()
        store.add(namespace="n", owner_agent="a", kind="fact", content="Generic note", importance=1.0, now=self.now)
        store.add(namespace="n", owner_agent="a", kind="fact", content="Redis memory backend", tags=["redis"], importance=0.7, now=self.now)

        results = store.retrieve(MemoryQuery(namespace="n", text="redis backend", limit=2))

        self.assertEqual(results[0].record.content, "Redis memory backend")

    def test_context_pack_is_prompt_ready(self) -> None:
        store = build_demo_store()
        pack = build_context_memory_pack(store, "user:alice", "format structuré bootcamp")

        self.assertTrue(pack)
        self.assertTrue(all({"id", "kind", "content", "score", "reasons"}.issubset(item) for item in pack))
        self.assertFalse(any("Bob" in item["content"] for item in pack))


if __name__ == "__main__":
    unittest.main(verbosity=2)
