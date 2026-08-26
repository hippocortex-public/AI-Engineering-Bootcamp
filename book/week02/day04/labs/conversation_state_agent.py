"""
Semaine 2 — Jour 4 : Conversation State

Mini-agent de support client stateful.

Objectifs :
- maintenir un état conversationnel explicite ;
- collecter progressivement les slots nécessaires ;
- décider la prochaine réponse à partir de l'état ;
- sérialiser/restaurer la session ;
- refuser une action métier tant que l'état est incomplet.

Aucune dépendance externe n'est requise.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import re
from typing import Any, Literal


Intent = Literal["unknown", "order_status", "refund", "technical_issue"]
Status = Literal["collecting", "ready_for_action", "completed", "blocked"]
Role = Literal["user", "assistant"]


REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "order_status": ("order_id", "email"),
    "refund": ("order_id", "email", "reason"),
    "technical_issue": ("email", "issue_summary"),
}

QUESTION_BY_FIELD: dict[str, str] = {
    "order_id": "Quel est votre numéro de commande ?",
    "email": "Quelle adresse email est associée à la demande ?",
    "reason": "Quelle est la raison de votre demande de remboursement ?",
    "issue_summary": "Pouvez-vous décrire brièvement le problème technique ?",
}

ORDER_ID_RE = re.compile(r"\b(?:ORD|CMD)[-\s]?\d{3,}\b", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")


class ConversationStateError(ValueError):
    """Raised when a conversation state cannot be used safely."""


@dataclass(frozen=True)
class Message:
    """Single chat message stored in the short-term conversation history."""

    role: Role
    content: str

    def to_dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Message":
        role = data.get("role")
        content = data.get("content")

        if role not in {"user", "assistant"}:
            raise ConversationStateError(f"Invalid message role: {role!r}")
        if not isinstance(content, str):
            raise ConversationStateError("Message content must be a string")

        return cls(role=role, content=content)


@dataclass
class ConversationState:
    """
    Application-owned state for one conversation.

    This object is intentionally small.
    It stores what the backend needs to continue a multi-turn workflow.
    """

    session_id: str
    user_id: str
    intent: Intent = "unknown"
    slots: dict[str, str] = field(default_factory=dict)
    messages: list[Message] = field(default_factory=list)
    tool_results: dict[str, dict[str, Any]] = field(default_factory=dict)
    turn_count: int = 0
    status: Status = "collecting"

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "intent": self.intent,
            "slots": dict(self.slots),
            "messages": [message.to_dict() for message in self.messages],
            "tool_results": self.tool_results,
            "turn_count": self.turn_count,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConversationState":
        required = {
            "session_id",
            "user_id",
            "intent",
            "slots",
            "messages",
            "tool_results",
            "turn_count",
            "status",
        }
        missing = required - set(data)
        if missing:
            raise ConversationStateError(
                f"Missing required state fields: {sorted(missing)}"
            )

        intent = data["intent"]
        if intent not in {"unknown", "order_status", "refund", "technical_issue"}:
            raise ConversationStateError(f"Invalid intent: {intent!r}")

        status = data["status"]
        if status not in {"collecting", "ready_for_action", "completed", "blocked"}:
            raise ConversationStateError(f"Invalid status: {status!r}")

        if not isinstance(data["slots"], dict):
            raise ConversationStateError("slots must be a dictionary")
        if not isinstance(data["tool_results"], dict):
            raise ConversationStateError("tool_results must be a dictionary")
        if not isinstance(data["messages"], list):
            raise ConversationStateError("messages must be a list")
        if not isinstance(data["turn_count"], int) or data["turn_count"] < 0:
            raise ConversationStateError("turn_count must be a non-negative integer")

        return cls(
            session_id=str(data["session_id"]),
            user_id=str(data["user_id"]),
            intent=intent,
            slots={str(key): str(value) for key, value in data["slots"].items()},
            messages=[Message.from_dict(item) for item in data["messages"]],
            tool_results=dict(data["tool_results"]),
            turn_count=data["turn_count"],
            status=status,
        )


def initialize_state(session_id: str, user_id: str) -> ConversationState:
    """Create a new isolated conversation state."""

    if not session_id:
        raise ConversationStateError("session_id is required")
    if not user_id:
        raise ConversationStateError("user_id is required")

    return ConversationState(session_id=session_id, user_id=user_id)


def normalize_order_id(value: str) -> str:
    """Normalize command identifiers to a consistent ORD-1234/CMD-1234 style."""

    cleaned = value.upper().replace(" ", "-")
    if "-" not in cleaned:
        cleaned = f"{cleaned[:3]}-{cleaned[3:]}"
    return cleaned


def detect_intent(message: str, current_intent: Intent = "unknown") -> Intent:
    """
    Detect the user's intent.

    If the current intent is already known and the new message is only a slot,
    keep the existing intent.
    """

    text = message.lower()

    refund_keywords = ["remboursement", "rembourser", "refund", "facturé", "facturee", "double"]
    order_keywords = ["suivre", "suivi", "statut", "commande", "livraison", "order status"]
    technical_keywords = ["bug", "erreur", "connecter", "connexion", "technique", "ne marche pas", "crash"]

    if any(keyword in text for keyword in refund_keywords):
        return "refund"
    if any(keyword in text for keyword in technical_keywords):
        return "technical_issue"
    if any(keyword in text for keyword in order_keywords):
        return "order_status"

    return current_intent


def extract_slots(message: str, intent: Intent, existing_slots: dict[str, str] | None = None) -> dict[str, str]:
    """
    Extract simple slots from a user message.

    This function is intentionally deterministic.
    In production, a model could produce a structured extraction instead.
    """

    existing_slots = existing_slots or {}
    slots: dict[str, str] = {}
    text = message.strip()
    lower = text.lower()

    order_match = ORDER_ID_RE.search(text)
    if order_match:
        slots["order_id"] = normalize_order_id(order_match.group(0))

    email_match = EMAIL_RE.search(text)
    if email_match:
        slots["email"] = email_match.group(0).lower()

    if intent == "refund":
        if any(term in lower for term in ["double", "deux fois", "facturé deux", "facturee deux"]):
            slots["reason"] = "double_billing"
        elif any(term in lower for term in ["cassé", "casse", "endommagé", "defectueux", "défectueux"]):
            slots["reason"] = "damaged_item"
        elif "reason" not in existing_slots and _looks_like_reason(text):
            slots["reason"] = text

    if intent == "technical_issue":
        if "issue_summary" not in existing_slots and _looks_like_issue_summary(text):
            slots["issue_summary"] = text

    return slots


def _looks_like_reason(message: str) -> bool:
    """Heuristic for accepting a message as a refund reason."""

    lower = message.lower()
    if EMAIL_RE.search(message) or ORDER_ID_RE.search(message):
        return False

    # Generic intent declarations are not valid refund reasons.
    generic_requests = [
        "je veux un remboursement",
        "je souhaite un remboursement",
        "remboursement",
        "refund",
    ]
    if lower.strip(" .!?") in generic_requests:
        return False

    return any(
        marker in lower
        for marker in [
            "car ",
            "parce que",
            "j'ai",
            "je n'ai",
            "produit",
            "article",
            "facture",
            "facturé",
            "abîmé",
            "abime",
        ]
    ) or len(message.split()) >= 5


def _looks_like_issue_summary(message: str) -> bool:
    """Heuristic for accepting a message as a technical issue summary."""

    lower = message.lower()
    if EMAIL_RE.search(message) or ORDER_ID_RE.search(message):
        return False
    return any(
        marker in lower
        for marker in [
            "erreur",
            "bug",
            "connexion",
            "connecter",
            "crash",
            "ne marche",
            "bloqué",
            "bloque",
        ]
    ) or len(message.split()) >= 5


def missing_required_fields(state: ConversationState) -> list[str]:
    """Return required fields that are not yet present for the current intent."""

    if state.intent == "unknown":
        return ["intent"]

    required = REQUIRED_FIELDS[state.intent]
    return [field_name for field_name in required if field_name not in state.slots]


def next_assistant_message(state: ConversationState) -> str:
    """Choose the next assistant response from the current state."""

    missing = missing_required_fields(state)

    if not missing:
        if state.intent == "refund":
            return "Merci, j’ai les informations nécessaires pour traiter la demande de remboursement."
        if state.intent == "order_status":
            return "Merci, j’ai les informations nécessaires pour vérifier le suivi de commande."
        if state.intent == "technical_issue":
            return "Merci, j’ai les informations nécessaires pour transmettre le problème technique."
        return "Merci, j’ai les informations nécessaires."

    first_missing = missing[0]

    if first_missing == "intent":
        return (
            "Pouvez-vous préciser si votre demande concerne un suivi de commande, "
            "un remboursement ou un problème technique ?"
        )

    return QUESTION_BY_FIELD[first_missing]


def handle_user_message(
    state: ConversationState,
    user_message: str,
) -> tuple[ConversationState, str]:
    """
    Process one user turn and update the conversation state.

    The function mutates and returns the provided state for pedagogical simplicity.
    A production system may prefer immutable updates.
    """

    if not user_message or not user_message.strip():
        raise ConversationStateError("user_message cannot be empty")

    state.messages.append(Message(role="user", content=user_message))
    state.turn_count += 1

    new_intent = detect_intent(user_message, state.intent)
    state.intent = new_intent

    extracted_slots = extract_slots(user_message, state.intent, state.slots)
    state.slots.update(extracted_slots)

    state.status = "ready_for_action" if not missing_required_fields(state) else "collecting"

    reply = next_assistant_message(state)
    state.messages.append(Message(role="assistant", content=reply))
    return state, reply


def serialize_state(state: ConversationState) -> str:
    """Serialize a conversation state to JSON."""

    return json.dumps(state.to_dict(), ensure_ascii=False, sort_keys=True)


def restore_state(payload: str) -> ConversationState:
    """Restore a conversation state from JSON."""

    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ConversationStateError("State payload is not valid JSON") from exc

    if not isinstance(data, dict):
        raise ConversationStateError("State payload must decode to an object")

    return ConversationState.from_dict(data)


def execute_ready_action(state: ConversationState) -> dict[str, Any]:
    """
    Simulate a business action.

    The action is allowed only when the state is complete.
    """

    missing = missing_required_fields(state)
    if missing:
        raise ConversationStateError(
            f"Cannot execute action: missing fields {missing}"
        )

    if state.status != "ready_for_action":
        raise ConversationStateError(
            f"Cannot execute action from status {state.status!r}"
        )

    result = {
        "intent": state.intent,
        "session_id": state.session_id,
        "accepted_slots": dict(state.slots),
        "action_status": "accepted",
    }

    state.tool_results["business_action"] = result
    state.status = "completed"
    return result


def demo() -> None:
    """Run a small multi-turn conversation."""

    state = initialize_state("session_demo", "user_demo")

    for user_message in [
        "Je veux un remboursement.",
        "ORD-1001",
        "lea@example.com",
        "J'ai été facturée deux fois.",
    ]:
        state, reply = handle_user_message(state, user_message)
        print(f"Utilisateur: {user_message}")
        print(f"Assistant:   {reply}")
        print(f"State:       intent={state.intent}, slots={state.slots}, status={state.status}")
        print("---")

    action = execute_ready_action(state)
    print("Action:", action)


if __name__ == "__main__":
    demo()
