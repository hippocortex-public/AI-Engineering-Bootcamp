import unittest

from ai_persistence.domain import MessageRole, RunStatus
from ai_persistence.repository import InMemoryConversationStore


class RepositoryContractTest(unittest.TestCase):
    def test_create_conversation_and_append_messages(self):
        store = InMemoryConversationStore()
        conversation = store.create_conversation(
            tenant_id="tenant-acme",
            user_id="user-42",
            title="Incident analysis",
        )

        store.append_message(conversation.id, MessageRole.USER, "Analyse cet incident.")
        store.append_message(conversation.id, MessageRole.ASSISTANT, "Voici l'analyse.")

        messages = store.list_messages(conversation.id)

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].role, MessageRole.USER)
        self.assertEqual(messages[1].role, MessageRole.ASSISTANT)

    def test_message_requires_existing_conversation(self):
        store = InMemoryConversationStore()
        with self.assertRaises(KeyError):
            store.append_message("missing", MessageRole.USER, "Bonjour")

    def test_run_and_tool_call_lifecycle(self):
        store = InMemoryConversationStore()
        conversation = store.create_conversation("tenant", "user", "Demo")

        run = store.create_agent_run(
            conversation_id=conversation.id,
            model="demo-model",
            prompt_version="prompt-v1",
        )
        tool_call = store.add_tool_call(
            agent_run_id=run.id,
            tool_name="crm_lookup",
            arguments={"customer_id": "123"},
            result={"tier": "enterprise"},
        )
        completed = store.complete_agent_run(
            run.id,
            status=RunStatus.SUCCEEDED,
            input_tokens=120,
            output_tokens=80,
            latency_ms=900,
        )

        self.assertEqual(tool_call.status, RunStatus.SUCCEEDED)
        self.assertEqual(completed.status, RunStatus.SUCCEEDED)
        self.assertEqual(completed.output_tokens, 80)

    def test_final_status_must_be_terminal(self):
        store = InMemoryConversationStore()
        conversation = store.create_conversation("tenant", "user", "Demo")
        run = store.create_agent_run(conversation.id, "model", "v1")

        with self.assertRaises(ValueError):
            store.complete_agent_run(run.id, status=RunStatus.RUNNING)


if __name__ == "__main__":
    unittest.main()
