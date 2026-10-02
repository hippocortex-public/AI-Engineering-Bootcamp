import unittest

from ai_persistence.domain import AgentRun, Conversation, Message, MessageRole, RunStatus, ToolCall


class DomainTest(unittest.TestCase):
    def test_conversation_requires_tenant(self):
        with self.assertRaises(ValueError):
            Conversation(tenant_id="", user_id="user-1", title="Demo")

    def test_message_requires_valid_role_enum(self):
        conversation = Conversation(tenant_id="tenant", user_id="user", title="Demo")
        message = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content="Bonjour",
        )
        self.assertEqual(message.role, MessageRole.USER)

    def test_agent_run_rejects_negative_tokens(self):
        conversation = Conversation(tenant_id="tenant", user_id="user", title="Demo")
        with self.assertRaises(ValueError):
            AgentRun(
                conversation_id=conversation.id,
                model="demo-model",
                prompt_version="v1",
                input_tokens=-1,
            )

    def test_tool_call_requires_agent_run_id(self):
        with self.assertRaises(ValueError):
            ToolCall(agent_run_id="", tool_name="search", arguments={})


if __name__ == "__main__":
    unittest.main()
