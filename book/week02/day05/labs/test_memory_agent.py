"""
Tests déterministes pour le lab Memory courte, longue et state.

Exécution :
    python test_memory_agent.py
"""

from memory_agent import MemoryAwareSupportAgent, LongTermMemoryStore


def test_short_term_memory_is_bounded():
    agent = MemoryAwareSupportAgent(short_term_max_messages=4)

    agent.receive("u1", "message 1")
    agent.receive("u1", "message 2")
    agent.receive("u1", "message 3")

    context = agent.build_context("u1")
    assert len(context["recent_messages"]) == 4
    assert context["recent_messages"][0]["content"] != "message 1"


def test_display_name_is_persisted_in_long_term_memory():
    agent = MemoryAwareSupportAgent()

    response = agent.receive("u1", "Tu peux m'appeler Nadia.")

    assert agent.memory.get_profile("u1").display_name == "Nadia"
    assert response.startswith("Nadia,")


def test_language_preference_personalizes_future_response():
    agent = MemoryAwareSupportAgent()

    agent.receive("u1", "Je préfère les exemples en Python.")
    response = agent.receive("u1", "Aide-moi à créer un ticket.")

    assert "Python" in response


def test_user_preferences_are_isolated():
    agent = MemoryAwareSupportAgent()

    agent.receive("alice", "Je préfère les exemples en Python.")
    agent.receive("bob", "Je préfère les exemples en TypeScript.")

    alice_response = agent.receive("alice", "Aide-moi à créer un ticket.")
    bob_response = agent.receive("bob", "Aide-moi à créer un ticket.")

    assert "Python" in alice_response
    assert "TypeScript" in bob_response
    assert "TypeScript" not in alice_response
    assert "Python" not in bob_response


def test_conversation_state_tracks_missing_slots():
    agent = MemoryAwareSupportAgent()

    response = agent.receive("u1", "J'ai un problème.")

    state = agent.build_context("u1")["state"]
    assert state["intent"] == "create_support_ticket"
    assert state["status"] == "collecting"
    assert "product" in state["missing_slots"]
    assert "description" in state["missing_slots"]
    assert "product" in response
    assert "description" in response


def test_conversation_state_becomes_ready():
    agent = MemoryAwareSupportAgent()

    response = agent.receive("u1", "J'ai une erreur 500 avec Billing API.")

    state = agent.build_context("u1")["state"]
    assert state["intent"] == "create_support_ticket"
    assert state["slots"]["product"] == "Billing API"
    assert "500" in state["slots"]["description"]
    assert state["missing_slots"] == []
    assert state["status"] == "ready"
    assert "informations nécessaires" in response


def test_forget_user_removes_all_memory_layers():
    agent = MemoryAwareSupportAgent()

    agent.receive("u1", "Tu peux m'appeler Nadia.")
    agent.receive("u1", "Je préfère les exemples en Python.")
    agent.receive("u1", "J'ai une erreur 500 avec Billing API.")

    agent.forget_user("u1")
    context = agent.build_context("u1")

    assert context["profile"]["display_name"] is None
    assert context["profile"]["preferences"] == {}
    assert context["state"]["intent"] is None
    assert context["recent_messages"] == []


def test_memory_store_can_round_trip_json():
    store = LongTermMemoryStore()
    store.set_display_name("u1", "Nadia")
    store.set_preference("u1", "language", "Python")

    restored = LongTermMemoryStore.from_json(store.to_json())

    profile = restored.get_profile("u1")
    assert profile.display_name == "Nadia"
    assert profile.preferences["language"] == "Python"


def test_clear_current_state_keeps_long_term_memory():
    agent = MemoryAwareSupportAgent()

    agent.receive("u1", "Je préfère les exemples en Python.")
    agent.receive("u1", "J'ai une erreur 500 avec Billing API.")

    agent.clear_current_state("u1")
    context = agent.build_context("u1")

    assert context["profile"]["preferences"]["language"] == "Python"
    assert context["state"]["intent"] is None


def run_all_tests():
    tests = [
        test_short_term_memory_is_bounded,
        test_display_name_is_persisted_in_long_term_memory,
        test_language_preference_personalizes_future_response,
        test_user_preferences_are_isolated,
        test_conversation_state_tracks_missing_slots,
        test_conversation_state_becomes_ready,
        test_forget_user_removes_all_memory_layers,
        test_memory_store_can_round_trip_json,
        test_clear_current_state_keeps_long_term_memory,
    ]

    for test in tests:
        test()

    print(f"{len(tests)} tests passed")


if __name__ == "__main__":
    run_all_tests()
