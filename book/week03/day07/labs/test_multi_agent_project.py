import json
import unittest

from multi_agent_project import (
    ContextBuilder,
    DeliveryCoordinator,
    MCPToolAdapter,
    SharedStateStore,
    Task,
    ToolSpec,
    create_test_plan,
    default_tools,
)


class MultiAgentProjectTests(unittest.TestCase):
    def test_successful_project_returns_completed_status(self):
        coordinator = DeliveryCoordinator()
        result = coordinator.run(
            "Concevoir une architecture multi-agent avec MCP, état partagé, contexte contrôlé, sécurité et revue finale."
        )
        self.assertEqual(result["status"], "completed")
        self.assertGreaterEqual(result["review"]["score"], 0.8)

    def test_result_contains_required_artifacts(self):
        coordinator = DeliveryCoordinator()
        result = coordinator.run(
            "Préparer un assistant multi-agent avec MCP, state sharing, context engineering et tests."
        )
        names = {artifact["name"] for artifact in result["artifacts"]}
        expected = {
            "delivery_plan",
            "research_notes",
            "architecture_proposal",
            "test_plan",
            "security_review",
            "final_review",
        }
        self.assertTrue(expected.issubset(names))

    def test_short_objective_needs_clarification(self):
        coordinator = DeliveryCoordinator()
        result = coordinator.run("MCP")
        self.assertEqual(result["status"], "needs_clarification")
        self.assertEqual(result["review"]["verdict"], "needs_clarification")

    def test_empty_objective_raises(self):
        coordinator = DeliveryCoordinator()
        with self.assertRaises(ValueError):
            coordinator.run("   ")

    def test_tool_list_is_deterministic(self):
        state = SharedStateStore()
        adapter = MCPToolAdapter(default_tools(), state)
        first = [tool["name"] for tool in adapter.list_tools()]
        second = [tool["name"] for tool in adapter.list_tools()]
        self.assertEqual(first, second)
        self.assertEqual(first, sorted(first))

    def test_mcp_adapter_validates_required_arguments(self):
        state = SharedStateStore()
        adapter = MCPToolAdapter(default_tools(), state)
        with self.assertRaises(ValueError):
            adapter.call("create_test_plan", {}, actor="tester")

    def test_sensitive_tool_is_blocked_without_approval(self):
        coordinator = DeliveryCoordinator()
        result = coordinator.run(
            "Préparer un déploiement d'architecture multi-agent avec MCP et validation sécurité.",
            approved_actions=False,
        )
        self.assertEqual(result["status"], "blocked_by_policy")
        events = [event["event"] for event in result["trace"]]
        self.assertIn("tool_blocked", events)

    def test_sensitive_tool_passes_with_approval(self):
        coordinator = DeliveryCoordinator()
        result = coordinator.run(
            "Préparer un déploiement d'architecture multi-agent avec MCP, état partagé et validation sécurité.",
            approved_actions=True,
        )
        self.assertEqual(result["status"], "completed")
        names = [artifact["name"] for artifact in result["artifacts"]]
        self.assertIn("deployment_approval", names)

    def test_private_state_is_not_visible_to_other_roles(self):
        state = SharedStateStore()
        state.put("secret", {"token": "hidden"}, owner="researcher", visibility="private")
        state.put("public", {"value": 1}, owner="coordinator", visibility="public")
        self.assertIn("secret", state.snapshot_for("researcher"))
        self.assertNotIn("secret", state.snapshot_for("engineer"))
        self.assertIn("public", state.snapshot_for("engineer"))

    def test_state_version_increments(self):
        state = SharedStateStore()
        first = state.put("plan", {"v": 1}, owner="planner", visibility="public")
        second = state.put("plan", {"v": 2}, owner="planner", visibility="public")
        self.assertEqual(first.version, 1)
        self.assertEqual(second.version, 2)

    def test_context_builder_respects_budget(self):
        state = SharedStateStore()
        state.put("objective", "x" * 100, owner="coordinator", visibility="public")
        state.put("large", "y" * 1000, owner="researcher", visibility="shared", readers=["engineer"])
        builder = ContextBuilder(state, max_chars=250)
        context = builder.build(
            "engineer",
            Task(title="architecture", owner="engineer", goal="build", required_tools=[]),
            [],
        )
        self.assertLessEqual(context["budget"]["used_chars"], 250)

    def test_context_contains_only_task_tools(self):
        state = SharedStateStore()
        state.put("objective", "Construire un projet multi-agent", owner="coordinator", visibility="public")
        builder = ContextBuilder(state, max_chars=500)
        context = builder.build(
            "engineer",
            Task(
                title="architecture",
                owner="engineer",
                goal="build",
                required_tools=["generate_architecture"],
            ),
            [
                {"name": "generate_architecture", "required": [], "description": "", "sensitive": False},
                {"name": "search_knowledge_base", "required": [], "description": "", "sensitive": False},
            ],
        )
        self.assertEqual([tool["name"] for tool in context["tools"]], ["generate_architecture"])

    def test_trace_is_json_serializable(self):
        coordinator = DeliveryCoordinator()
        result = coordinator.run(
            "Concevoir une architecture multi-agent avec MCP, état partagé et revue qualité."
        )
        encoded = json.dumps(result["trace"], ensure_ascii=False)
        self.assertIn("run_started", encoded)
        self.assertIn("run_finished", encoded)

    def test_review_fails_when_required_context_missing(self):
        # On force une revue sans artefacts préalables.
        coordinator = DeliveryCoordinator()
        task = Task(title="final_review", owner="reviewer", goal="review")
        context = coordinator.context_builder.build("reviewer", task, coordinator.tools.list_tools())
        review = coordinator.agents["reviewer"].run(task, context)
        self.assertEqual(review.content["verdict"], "needs_revision")
        self.assertLess(review.content["score"], 0.8)

    def test_custom_tool_can_be_registered(self):
        state = SharedStateStore()

        def echo(arguments):
            return {"echo": arguments["message"]}

        adapter = MCPToolAdapter(
            [
                ToolSpec(
                    name="echo",
                    description="Echo tool",
                    required=["message"],
                    handler=echo,
                )
            ],
            state,
        )
        result = adapter.call("echo", {"message": "hello"}, actor="tester")
        self.assertEqual(result["echo"], "hello")


if __name__ == "__main__":
    unittest.main(verbosity=2)
