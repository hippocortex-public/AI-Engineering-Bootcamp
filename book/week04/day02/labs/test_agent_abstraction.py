import unittest

from agent_abstraction import (
    Agent,
    AgentResult,
    EchoModelClient,
    ModelRequest,
    ModelResponse,
    RunContext,
)


class FailingModelClient:
    def complete(self, request: ModelRequest) -> ModelResponse:
        raise RuntimeError("simulated provider failure")


class AgentAbstractionTests(unittest.TestCase):
    def make_agent(self, client=None, **overrides):
        return Agent(
            name=overrides.get("name", "explainer"),
            instructions=overrides.get(
                "instructions",
                "Explique simplement les concepts AI Engineering avec un exemple.",
            ),
            model_client=client or EchoModelClient("réponse contrôlée"),
            model=overrides.get("model", "fake-model"),
            max_input_chars=overrides.get("max_input_chars", 200),
            metadata=overrides.get("metadata", {"team": "bootcamp"}),
        )

    def make_context(self, text="Explique agent vs workflow."):
        return RunContext(
            user_input=text,
            session_id="s1",
            user_id="u1",
            metadata={"exercise": "unit-test"},
        )

    def test_agent_returns_standard_result(self):
        agent = self.make_agent()
        result = agent.run(self.make_context())
        self.assertIsInstance(result, AgentResult)
        self.assertEqual(result.agent_name, "explainer")
        self.assertEqual(result.status, "completed")
        self.assertEqual(result.output, "réponse contrôlée")
        self.assertIn("input_chars", result.usage)
        self.assertIn("output_chars", result.usage)
        self.assertGreaterEqual(len(result.trace), 4)

    def test_model_client_is_called_once(self):
        client = EchoModelClient("ok")
        agent = self.make_agent(client=client)
        result = agent.run(self.make_context())
        self.assertEqual(result.status, "completed")
        self.assertEqual(len(client.calls), 1)

    def test_build_messages_is_deterministic(self):
        agent = self.make_agent()
        context = self.make_context("  Bonjour agent.  ")
        messages = agent.build_messages(context)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["role"], "user")
        self.assertEqual(messages[1]["content"], "Bonjour agent.")

    def test_request_metadata_contains_context(self):
        client = EchoModelClient("ok")
        agent = self.make_agent(client=client)
        agent.run(self.make_context())
        request = client.calls[0]
        self.assertEqual(request.metadata["agent_name"], "explainer")
        self.assertEqual(request.metadata["session_id"], "s1")
        self.assertEqual(request.metadata["user_id"], "u1")
        self.assertEqual(request.metadata["exercise"], "unit-test")

    def test_empty_input_is_blocked(self):
        client = EchoModelClient("should not be called")
        agent = self.make_agent(client=client)
        result = agent.run(self.make_context("   "))
        self.assertEqual(result.status, "blocked")
        self.assertEqual(result.output, "")
        self.assertEqual(len(client.calls), 0)
        self.assertIn("empty", result.metadata["reason"])

    def test_too_long_input_is_blocked(self):
        client = EchoModelClient("should not be called")
        agent = self.make_agent(client=client, max_input_chars=5)
        result = agent.run(self.make_context("message trop long"))
        self.assertEqual(result.status, "blocked")
        self.assertEqual(len(client.calls), 0)
        self.assertIn("exceeds", result.metadata["reason"])

    def test_unsafe_database_instruction_is_blocked(self):
        client = EchoModelClient("should not be called")
        agent = self.make_agent(client=client)
        result = agent.run(self.make_context("Peux-tu faire DROP TABLE users ?"))
        self.assertEqual(result.status, "blocked")
        self.assertEqual(len(client.calls), 0)
        self.assertIn("Unsafe database", result.metadata["reason"])

    def test_invalid_agent_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.make_agent(name="Bad Name")

    def test_invalid_instructions_are_rejected(self):
        with self.assertRaises(ValueError):
            self.make_agent(instructions="court")

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            AgentResult(
                agent_name="a",
                output="x",
                status="unknown",
                usage={},
                trace=[],
            )

    def test_provider_failure_returns_failed_status(self):
        agent = self.make_agent(client=FailingModelClient())
        result = agent.run(self.make_context())
        self.assertEqual(result.status, "failed")
        self.assertIn("simulated provider failure", result.metadata["error"])

    def test_result_is_json_serializable(self):
        agent = self.make_agent()
        result = agent.run(self.make_context())
        payload = result.to_json()
        self.assertIn('"agent_name": "explainer"', payload)
        self.assertIn('"status": "completed"', payload)


if __name__ == "__main__":
    unittest.main(verbosity=2)
