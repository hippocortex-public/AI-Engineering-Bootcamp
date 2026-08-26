"""
Tests du lab Conversation State.

Exécution :
    python test_conversation_state_agent.py
"""

from conversation_state_agent import (
    ConversationStateError,
    execute_ready_action,
    handle_user_message,
    initialize_state,
    missing_required_fields,
    restore_state,
    serialize_state,
)


def assert_raises(expected_exception, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except expected_exception:
        return
    except Exception as exc:
        raise AssertionError(
            f"Expected {expected_exception.__name__}, got {type(exc).__name__}: {exc}"
        ) from exc

    raise AssertionError(f"Expected {expected_exception.__name__} to be raised")


def test_refund_flow_collects_slots_over_multiple_turns():
    state = initialize_state("session_001", "user_123")

    state, reply = handle_user_message(state, "Je veux un remboursement.")
    assert state.intent == "refund"
    assert state.status == "collecting"
    assert "numéro de commande" in reply

    state, reply = handle_user_message(state, "ORD-1001")
    assert state.slots["order_id"] == "ORD-1001"
    assert state.intent == "refund"
    assert "email" in reply.lower()

    state, reply = handle_user_message(state, "lea@example.com")
    assert state.slots["email"] == "lea@example.com"
    assert "raison" in reply.lower()

    state, reply = handle_user_message(state, "J'ai été facturée deux fois.")
    assert state.slots["reason"] == "double_billing"
    assert state.status == "ready_for_action"
    assert "informations nécessaires" in reply


def test_missing_required_fields_are_computed_from_intent_and_slots():
    state = initialize_state("session_002", "user_123")
    state.intent = "refund"
    state.slots["order_id"] = "ORD-1001"

    assert missing_required_fields(state) == ["email", "reason"]


def test_action_is_rejected_when_state_is_incomplete():
    state = initialize_state("session_003", "user_123")
    state, _ = handle_user_message(state, "Je veux suivre ma commande.")
    state, _ = handle_user_message(state, "ORD-1001")

    assert state.status == "collecting"
    assert_raises(ConversationStateError, execute_ready_action, state)


def test_action_is_allowed_when_state_is_ready():
    state = initialize_state("session_004", "user_123")
    state, _ = handle_user_message(state, "Je veux suivre ma commande.")
    state, _ = handle_user_message(state, "ORD-1001")
    state, _ = handle_user_message(state, "lea@example.com")

    assert state.status == "ready_for_action"

    result = execute_ready_action(state)

    assert result["intent"] == "order_status"
    assert result["action_status"] == "accepted"
    assert state.status == "completed"
    assert "business_action" in state.tool_results


def test_state_can_be_serialized_and_restored():
    state = initialize_state("session_005", "user_123")
    state, _ = handle_user_message(state, "J'ai un problème technique.")
    state, _ = handle_user_message(state, "lea@example.com")
    state, _ = handle_user_message(state, "Je ne peux plus me connecter à mon compte.")

    payload = serialize_state(state)
    restored = restore_state(payload)

    assert restored.session_id == state.session_id
    assert restored.user_id == state.user_id
    assert restored.intent == "technical_issue"
    assert restored.slots == state.slots
    assert restored.status == "ready_for_action"
    assert restored.turn_count == 3
    assert len(restored.messages) == len(state.messages)


def test_two_sessions_do_not_share_slots():
    state_a = initialize_state("session_A", "alice")
    state_b = initialize_state("session_B", "bob")

    state_a, _ = handle_user_message(state_a, "Je veux suivre ma commande ORD-1001 avec alice@example.com.")
    state_b, _ = handle_user_message(state_b, "Je veux un remboursement.")

    assert state_a.slots["email"] == "alice@example.com"
    assert "email" not in state_b.slots
    assert state_a.session_id != state_b.session_id


def test_unknown_intent_asks_for_clarification():
    state = initialize_state("session_006", "user_123")
    state, reply = handle_user_message(state, "Bonjour, pouvez-vous m'aider ?")

    assert state.intent == "unknown"
    assert missing_required_fields(state) == ["intent"]
    assert "suivi de commande" in reply


def test_invalid_serialized_payload_is_rejected():
    assert_raises(ConversationStateError, restore_state, "{not valid json}")


def run_all_tests():
    test_refund_flow_collects_slots_over_multiple_turns()
    test_missing_required_fields_are_computed_from_intent_and_slots()
    test_action_is_rejected_when_state_is_incomplete()
    test_action_is_allowed_when_state_is_ready()
    test_state_can_be_serialized_and_restored()
    test_two_sessions_do_not_share_slots()
    test_unknown_intent_asks_for_clarification()
    test_invalid_serialized_payload_is_rejected()
    print("8 tests passed")


if __name__ == "__main__":
    run_all_tests()
