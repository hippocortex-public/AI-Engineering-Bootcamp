# Corrigé — Challenge

## Solution complète

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:
    user_input: str
    action: str | None = None
    observation: dict[str, Any] | None = None
    final_answer: str | None = None
    trace: list[str] = field(default_factory=list)


def extract_order_id(text: str) -> str:
    normalized = text.replace("?", " ").replace(".", " ")
    for token in normalized.split():
        if token.isdigit():
            return token
    return "unknown"


def extract_sku(text: str) -> str:
    normalized = text.replace("?", " ").replace(".", " ")
    for token in normalized.split():
        if token.upper().startswith("SKU-"):
            return token.upper()
    return "UNKNOWN"


def lookup_order(order_id: str) -> dict[str, str]:
    return {
        "order_id": order_id,
        "status": "expédiée",
        "eta": "2026-07-05",
    }


def lookup_inventory(sku: str) -> dict[str, Any]:
    return {
        "sku": sku,
        "available": True,
        "quantity": 12,
    }


def decide_action(user_input: str) -> str:
    text = user_input.lower()

    if "commande" in text:
        return "lookup_order"

    if "produit" in text or "stock" in text or "sku-" in text:
        return "lookup_inventory"

    return "answer_directly"


def run_agent(user_input: str) -> AgentState:
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


def test_order_request() -> None:
    state = run_agent("Où est ma commande 123 ?")
    assert state.action == "lookup_order"
    assert state.observation["order_id"] == "123"
    assert "called_tool:lookup_order" in state.trace


def test_inventory_request() -> None:
    state = run_agent("Le produit SKU-42 est-il disponible ?")
    assert state.action == "lookup_inventory"
    assert state.observation["sku"] == "SKU-42"
    assert "called_tool:lookup_inventory" in state.trace


def test_direct_request() -> None:
    state = run_agent("Bonjour")
    assert state.action == "answer_directly"
    assert state.observation is None
    assert state.final_answer is not None


if __name__ == "__main__":
    test_order_request()
    test_inventory_request()
    test_direct_request()
    print("All tests passed.")
```

## Points importants

Cette solution reste volontairement déterministe.

Elle prépare les journées suivantes, où la sélection d’action sera progressivement remplacée ou augmentée par :

- function calling ;
- sorties structurées ;
- gestion d’état ;
- mémoire ;
- boucle agentique.
