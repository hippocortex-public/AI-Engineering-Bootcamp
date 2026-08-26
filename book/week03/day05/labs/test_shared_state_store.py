import json
import unittest

from shared_state_store import (
    ConflictError,
    LocalAgentWorkspace,
    MissingKeyError,
    PermissionDenied,
    SharedStateStore,
    run_demo,
)


class SharedStateStoreTest(unittest.TestCase):
    def test_first_write_creates_version_one(self):
        store = SharedStateStore()
        entry = store.write(
            agent="triage",
            key="incident.summary",
            value="Erreur 500",
            visibility="shared",
        )
        self.assertEqual(entry.version, 1)
        self.assertEqual(entry.owner, "triage")

    def test_write_increments_version(self):
        store = SharedStateStore()
        store.write(agent="triage", key="incident.status", value="new")
        entry = store.write(agent="backend", key="incident.status", value="investigating")
        self.assertEqual(entry.version, 2)
        self.assertEqual(entry.updated_by, "backend")

    def test_compare_and_set_detects_conflict(self):
        store = SharedStateStore()
        store.write(agent="triage", key="plan.next_step", value="inspect logs")
        store.write(
            agent="backend",
            key="plan.next_step",
            value="inspect database",
            expected_version=1,
        )
        with self.assertRaises(ConflictError):
            store.write(
                agent="security",
                key="plan.next_step",
                value="rotate credentials",
                expected_version=1,
            )

    def test_private_entry_is_visible_to_owner(self):
        store = SharedStateStore()
        store.write(
            agent="triage",
            key="triage.private_notes",
            value="hypothèse non validée",
            visibility="private",
            owner="triage",
        )
        entry = store.read(agent="triage", key="triage.private_notes")
        self.assertEqual(entry.value, "hypothèse non validée")

    def test_private_entry_is_not_visible_to_other_agent(self):
        store = SharedStateStore()
        store.write(
            agent="triage",
            key="triage.private_notes",
            value="hypothèse non validée",
            visibility="private",
            owner="triage",
        )
        with self.assertRaises(PermissionDenied):
            store.read(agent="backend", key="triage.private_notes")

    def test_snapshot_filters_private_keys(self):
        store = SharedStateStore()
        store.write(
            agent="triage",
            key="triage.private_notes",
            value="brouillon",
            visibility="private",
            owner="triage",
        )
        store.write(
            agent="triage",
            key="incident.summary",
            value="Erreur checkout",
            visibility="shared",
        )
        snapshot = store.snapshot(agent="backend")
        self.assertIn("incident.summary", snapshot)
        self.assertNotIn("triage.private_notes", snapshot)

    def test_handoff_is_minimal_and_filtered(self):
        store = SharedStateStore()
        store.write(agent="coordinator", key="objective", value="Diagnostiquer", visibility="public")
        store.write(agent="triage", key="incident.summary", value="Erreur checkout", visibility="shared")
        store.write(
            agent="triage",
            key="triage.private_notes",
            value="brouillon",
            visibility="private",
            owner="triage",
        )
        handoff = store.create_handoff(
            from_agent="triage",
            to_agent="backend",
            keys=["objective", "incident.summary", "triage.private_notes", "missing.key"],
        )
        self.assertEqual(set(handoff["context"].keys()), {"objective", "incident.summary"})

    def test_patch_is_atomic_when_conflict_occurs(self):
        store = SharedStateStore()
        store.write(agent="triage", key="a", value=1)
        store.write(agent="triage", key="b", value=1)

        with self.assertRaises(ConflictError):
            store.apply_patch(
                agent="backend",
                writes={
                    "a": {"value": 2, "expected_version": 1},
                    "b": {"value": 2, "expected_version": 0},
                },
            )

        self.assertEqual(store.read(agent="backend", key="a").value, 1)
        self.assertEqual(store.read(agent="backend", key="b").value, 1)

    def test_successful_patch_applies_all_entries(self):
        store = SharedStateStore()
        result = store.apply_patch(
            agent="triage",
            writes={
                "incident.summary": {"value": "Erreur checkout", "visibility": "shared"},
                "incident.status": {"value": "investigating", "visibility": "public"},
            },
        )
        self.assertEqual(set(result.keys()), {"incident.summary", "incident.status"})
        self.assertEqual(store.read(agent="backend", key="incident.status").value, "investigating")

    def test_delete_removes_key_and_records_event(self):
        store = SharedStateStore()
        store.write(agent="triage", key="incident.status", value="new")
        store.delete(agent="coordinator", key="incident.status", expected_version=1)
        with self.assertRaises(MissingKeyError):
            store.read(agent="triage", key="incident.status")
        self.assertEqual(store.events()[-1]["operation"], "read")
        self.assertEqual(store.events()[-1]["status"], "missing")

    def test_local_workspace_is_not_shared_implicitly(self):
        workspace = LocalAgentWorkspace("triage")
        workspace.set_private_note("incident.summary", "Erreur checkout")
        store = SharedStateStore()
        self.assertNotIn("incident.summary", store.summary()["keys"])

        patch = workspace.export_patch(key="incident.summary", visibility="shared")
        store.apply_patch(agent="triage", writes=patch)
        self.assertIn("incident.summary", store.summary()["keys"])

    def test_export_as_mcp_resource_filters_private_keys(self):
        store = SharedStateStore()
        store.write(agent="coordinator", key="objective", value="Diagnostiquer", visibility="public")
        store.write(agent="triage", key="incident.summary", value="Erreur checkout", visibility="shared")
        store.write(
            agent="triage",
            key="triage.private_notes",
            value="brouillon",
            visibility="private",
            owner="triage",
        )
        resource = store.export_as_mcp_resource(uri="state://incident/current", agent="backend")
        payload = resource["text"]
        self.assertEqual(resource["mimeType"], "application/json")
        self.assertIn("objective", payload["state"])
        self.assertIn("incident.summary", payload["state"])
        self.assertNotIn("triage.private_notes", payload["state"])

    def test_summary_is_json_serializable_and_deterministic(self):
        store = SharedStateStore()
        store.write(agent="b", key="z", value=1)
        store.write(agent="a", key="a", value=2)
        summary = store.summary()
        self.assertEqual(summary["keys"], ["a", "z"])
        json.dumps(summary)

    def test_run_demo_contains_backend_snapshot_and_handoff(self):
        demo = run_demo()
        self.assertIn("backend_snapshot", demo)
        self.assertIn("incident.summary", demo["backend_snapshot"])
        self.assertNotIn("triage.private_notes", demo["backend_snapshot"])
        self.assertIn("handoff", demo)
        self.assertGreaterEqual(len(demo["events"]), 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
