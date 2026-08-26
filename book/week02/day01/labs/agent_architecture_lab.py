from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:
    """State container for a minimal mono-agent."""

    user_input: str
    action: str | None = None
    observation: dict[str, Any] | None = None
    final_answer: str | None = None
    trace: list[str] = field(default_factory=list)


def extract_order_id(text: str) -> str:
    """Extract the first numeric token from a text."""
    normalized = text.replace("?", " ").replace(".", " ")
    for token in normalized.split():
        if token.isdigit():
            return token
    return "unknown"


def extract_sku(text: str) -> str:
    """Extract a simple SKU-like token from a text."""
    normalized = text.replace("?", " ").replace(".", " ")
    for token in normalized.split():
        if token.upper().startswith("SKU-"):
            return token.upper()
    return "UNKNOWN"


def lookup_order(order_id: str) -> dict[str, str]:
    """Simulated order lookup tool."""
    return {
        "order_id": order_id,
        "status": "expédiée",
        "eta": "2026-07-05",
    }


def lookup_inventory(sku: str) -> dict[str, Any]:
    """Simulated inventory lookup tool."""
    return {
        "sku": sku,
        "available": True,
        "quantity": 12,
    }


def decide_action(user_input: str) -> str:
    """Select the next action using deterministic rules."""
    text = user_input.lower()

    if "commande" in text:
        return "lookup_order"

    if "produit" in text or "stock" in text or "sku-" in text:
        return "lookup_inventory"

    return "answer_directly"


def run_agent(user_input: str) -> AgentState:
    """Run a minimal mono-agent for one user request."""
    state = AgentState(user_input=user_input)
    state.trace.append("received_user_input")

    state.action = decide_action(user_input)
    state.trace.append(f"selected_action:{state.action}")

    if state.action == "lookup_order":
        order_id = extract_order_id(user_input)
        state.trace.append(f"extracted_order_id:{order_id}")

        state.observation = lookup_order(order_id)
        state.trace.append("called_tool:lookup_order")

        state.final_answer = (
            f"Votre commande {state.observation['order_id']} est "
            f"{state.observation['status']}. "
            f"Livraison estimée : {state.observation['eta']}."
        )
        state.trace.append("generated_final_answer")
        return state

    if state.action == "lookup_inventory":
        sku = extract_sku(user_input)
        state.trace.append(f"extracted_sku:{sku}")

        state.observation = lookup_inventory(sku)
        state.trace.append("called_tool:lookup_inventory")

        availability = "disponible" if state.observation["available"] else "indisponible"
        state.final_answer = (
            f"Le produit {state.observation['sku']} est {availability}. "
            f"Quantité disponible : {state.observation['quantity']}."
        )
        state.trace.append("generated_final_answer")
        return state

    state.final_answer = "Bonjour, je peux vous aider. Quelle est votre demande ?"
    state.trace.append("generated_final_answer")
    return state


def run_tests() -> None:
    order_state = run_agent("Où est ma commande 123 ?")
    assert order_state.action == "lookup_order"
    assert "commande 123" in order_state.final_answer
    assert "called_tool:lookup_order" in order_state.trace

    inventory_state = run_agent("Le produit SKU-42 est-il disponible ?")
    assert inventory_state.action == "lookup_inventory"
    assert "SKU-42" in inventory_state.final_answer
    assert "called_tool:lookup_inventory" in inventory_state.trace

    direct_state = run_agent("Bonjour")
    assert direct_state.action == "answer_directly"
    assert direct_state.observation is None
    assert "generated_final_answer" in direct_state.trace


if __name__ == "__main__":
    example = run_agent("Où est ma commande 123 ?")

    print("Final answer:")
    print(example.final_answer)
    print()

    print("Selected action:")
    print(example.action)
    print()

    print("Trace:")
    for event in example.trace:
        print(f"- {event}")

    run_tests()
    print()
    print("All tests passed.")
