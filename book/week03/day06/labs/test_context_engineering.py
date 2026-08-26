import unittest

from context_engineering import (
    ContextEngineer,
    ContextItem,
    ContextPack,
    ContextPolicy,
    build_demo_items,
    demo,
    estimate_tokens,
    normalize_content,
    redact_pii,
)


class ContextEngineeringTests(unittest.TestCase):
    def test_estimate_tokens_is_deterministic_and_positive(self):
        self.assertEqual(estimate_tokens(""), 0)
        self.assertGreater(estimate_tokens("hello world"), 0)
        self.assertEqual(estimate_tokens("hello world"), estimate_tokens("hello world"))

    def test_normalize_content_removes_case_and_extra_spaces(self):
        self.assertEqual(
            normalize_content("  Le Client ACME   "),
            normalize_content("le client acme"),
        )

    def test_redact_pii_masks_email_and_phone(self):
        text = "Contacte alice@example.com ou +33 6 12 34 56 78."
        redacted = redact_pii(text)
        self.assertIn("[REDACTED_EMAIL]", redacted)
        self.assertIn("[REDACTED_PHONE]", redacted)
        self.assertNotIn("alice@example.com", redacted)

    def test_private_items_are_not_selected_by_default(self):
        pack = demo()
        selected_ids = {item.id for item in pack.selected}
        dropped = {item.id: item.reason for item in pack.dropped}
        self.assertNotIn("private_security_note", selected_ids)
        self.assertEqual(dropped["private_security_note"], "visibility_not_allowed")

    def test_agent_target_filter_excludes_wrong_agent(self):
        engine = ContextEngineer(build_demo_items())
        policy = ContextPolicy(max_tokens=120, agent_name="router_agent")
        pack = engine.build("Router une demande facturation", policy)
        selected_ids = {item.id for item in pack.selected}
        self.assertNotIn("state_invoice", selected_ids)
        self.assertNotIn("billing_policy", selected_ids)

    def test_duplicate_items_are_dropped(self):
        engine = ContextEngineer(
            [
                ContextItem(
                    id="a",
                    kind="recent_message",
                    content="Le client ACME attend la facture.",
                    priority=80,
                ),
                ContextItem(
                    id="b",
                    kind="recent_message",
                    content=" le client acme attend la facture. ",
                    priority=70,
                ),
            ]
        )
        pack = engine.build("Répondre au client", ContextPolicy(max_tokens=100))
        self.assertEqual([item.id for item in pack.selected], ["a"])
        self.assertEqual(pack.dropped[0].reason, "duplicate")

    def test_budget_is_respected(self):
        items = [
            ContextItem(id="system", kind="system", content="règles " * 10, priority=100),
            ContextItem(id="state", kind="state", content="état " * 20, priority=95),
            ContextItem(id="resource", kind="resource", content="doc " * 80, priority=90),
        ]
        policy = ContextPolicy(max_tokens=50)
        pack = ContextEngineer(items).build("Traiter la demande", policy)
        self.assertLessEqual(pack.total_tokens, 50)
        self.assertIn("resource", {item.id for item in pack.dropped})

    def test_min_priority_excludes_low_value_tools(self):
        engine = ContextEngineer(build_demo_items())
        policy = ContextPolicy(max_tokens=160, min_priority=20, agent_name="billing_agent")
        pack = engine.build("Traiter facture", policy)
        dropped = {item.id: item.reason for item in pack.dropped}
        self.assertEqual(dropped["tool_delete_invoice"], "priority_too_low")

    def test_render_contains_sections_and_sources(self):
        pack = demo()
        rendered = pack.render()
        self.assertIn("# Context Pack", rendered)
        self.assertIn("## system", rendered)
        self.assertIn("source=policy", rendered)

    def test_pack_to_dict_contains_audit_data(self):
        pack = demo()
        data = pack.to_dict()
        self.assertIn("selected", data)
        self.assertIn("dropped", data)
        self.assertIn("total_tokens", data)
        self.assertIsInstance(data["dropped"], list)

    def test_validation_rejects_invalid_priority(self):
        engine = ContextEngineer()
        with self.assertRaises(ValueError):
            engine.add_item(
                ContextItem(
                    id="bad",
                    kind="memory",
                    content="invalid priority",
                    priority=101,
                )
            )

    def test_build_requires_positive_budget(self):
        engine = ContextEngineer()
        with self.assertRaises(ValueError):
            engine.build("goal", ContextPolicy(max_tokens=0))

    def test_context_pack_type(self):
        self.assertIsInstance(demo(), ContextPack)


if __name__ == "__main__":
    unittest.main(verbosity=2)
