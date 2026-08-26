"""
Semaine 2 — Jour 3 : Structured Outputs

Mini-agent de triage support.

Objectif :
- simuler une sortie structurée produite par un modèle ;
- parser le JSON ;
- valider un contrat de sortie ;
- mapper vers un objet métier Python ;
- refuser explicitement les sorties invalides.

Aucune dépendance externe n'est requise.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any


TRIAGE_OUTPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": [
        "category",
        "priority",
        "sentiment",
        "summary",
        "action_required",
        "next_action",
        "confidence",
    ],
    "additionalProperties": False,
    "properties": {
        "category": {
            "type": "string",
            "enum": ["billing", "technical", "account", "shipping", "other"],
        },
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high", "critical"],
        },
        "sentiment": {
            "type": "string",
            "enum": ["neutral", "frustrated", "angry", "satisfied"],
        },
        "summary": {"type": "string"},
        "action_required": {"type": "boolean"},
        "next_action": {
            "type": "object",
            "required": ["owner_team", "rationale"],
            "additionalProperties": False,
            "properties": {
                "owner_team": {
                    "type": "string",
                    "enum": [
                        "support_l1",
                        "billing_ops",
                        "technical_ops",
                        "account_ops",
                    ],
                },
                "rationale": {"type": "string"},
            },
        },
        "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
        },
    },
}


class StructuredOutputError(ValueError):
    """Raised when a model output cannot be used as a valid structured output."""


@dataclass(frozen=True)
class TriageDecision:
    """Validated business object consumed by the application."""

    category: str
    priority: str
    sentiment: str
    summary: str
    action_required: bool
    owner_team: str
    rationale: str
    confidence: float


def _type_matches(value: Any, expected_type: str) -> bool:
    """Validate a small useful subset of JSON Schema types."""

    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "number":
        # bool is a subclass of int in Python, so exclude it explicitly.
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    raise StructuredOutputError(f"Unsupported schema type: {expected_type}")


def validate_schema(data: Any, schema: dict[str, Any], path: str = "$") -> None:
    """
    Validate a small subset of JSON Schema.

    Supported keywords:
    - type
    - required
    - additionalProperties
    - properties
    - enum
    - minimum
    - maximum
    - items

    This is intentionally small and educational.
    In production, prefer a battle-tested validator.
    """

    expected_type = schema.get("type")
    if expected_type and not _type_matches(data, expected_type):
        raise StructuredOutputError(
            f"{path}: expected type {expected_type}, got {type(data).__name__}"
        )

    if "enum" in schema and data not in schema["enum"]:
        allowed = ", ".join(repr(item) for item in schema["enum"])
        raise StructuredOutputError(f"{path}: value {data!r} is not in enum [{allowed}]")

    if expected_type == "number":
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")

        if minimum is not None and data < minimum:
            raise StructuredOutputError(f"{path}: value {data!r} is lower than {minimum}")
        if maximum is not None and data > maximum:
            raise StructuredOutputError(f"{path}: value {data!r} is greater than {maximum}")

    if expected_type == "object":
        required = schema.get("required", [])
        properties = schema.get("properties", {})
        additional_properties = schema.get("additionalProperties", True)

        for field in required:
            if field not in data:
                raise StructuredOutputError(f"{path}: missing required field {field!r}")

        if additional_properties is False:
            allowed_keys = set(properties.keys())
            extra_keys = set(data.keys()) - allowed_keys
            if extra_keys:
                formatted = ", ".join(sorted(extra_keys))
                raise StructuredOutputError(f"{path}: unexpected field(s): {formatted}")

        for field, field_schema in properties.items():
            if field in data:
                validate_schema(data[field], field_schema, f"{path}.{field}")

    if expected_type == "array":
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(data):
                validate_schema(item, item_schema, f"{path}[{index}]")


def parse_triage_output(raw_output: str) -> TriageDecision:
    """Parse, validate and map a raw model output to a domain object."""

    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        raise StructuredOutputError(f"Invalid JSON: {exc.msg}") from exc

    validate_schema(data, TRIAGE_OUTPUT_SCHEMA)

    next_action = data["next_action"]

    return TriageDecision(
        category=data["category"],
        priority=data["priority"],
        sentiment=data["sentiment"],
        summary=data["summary"],
        action_required=data["action_required"],
        owner_team=next_action["owner_team"],
        rationale=next_action["rationale"],
        confidence=float(data["confidence"]),
    )


class MockStructuredModel:
    """
    Deterministic stand-in for an LLM.

    The goal is not to imitate a model perfectly.
    The goal is to make the structured-output pipeline executable and testable.
    """

    def generate(self, ticket: str) -> str:
        normalized = ticket.lower()

        if "facturé" in normalized or "facture" in normalized or "paiement" in normalized:
            payload = {
                "category": "billing",
                "priority": "high" if "énervé" in normalized or "colère" in normalized else "medium",
                "sentiment": "angry" if "énervé" in normalized or "colère" in normalized else "neutral",
                "summary": "Le client signale un problème de facturation.",
                "action_required": True,
                "next_action": {
                    "owner_team": "billing_ops",
                    "rationale": "Le ticket mentionne une facture ou un paiement.",
                },
                "confidence": 0.91,
            }
        elif "connecter" in normalized or "connexion" in normalized or "mot de passe" in normalized:
            payload = {
                "category": "technical",
                "priority": "high",
                "sentiment": "frustrated",
                "summary": "Le client rencontre un problème de connexion.",
                "action_required": True,
                "next_action": {
                    "owner_team": "technical_ops",
                    "rationale": "Le ticket indique un blocage d'accès.",
                },
                "confidence": 0.87,
            }
        elif "adresse" in normalized or "livraison" in normalized or "colis" in normalized:
            payload = {
                "category": "shipping",
                "priority": "medium",
                "sentiment": "neutral",
                "summary": "Le client pose une question liée à la livraison.",
                "action_required": True,
                "next_action": {
                    "owner_team": "support_l1",
                    "rationale": "Le support de premier niveau peut traiter la demande.",
                },
                "confidence": 0.79,
            }
        else:
            payload = {
                "category": "other",
                "priority": "low",
                "sentiment": "neutral",
                "summary": "Le ticket ne correspond pas à une catégorie spécifique.",
                "action_required": True,
                "next_action": {
                    "owner_team": "support_l1",
                    "rationale": "Une qualification humaine légère est nécessaire.",
                },
                "confidence": 0.62,
            }

        return json.dumps(payload, ensure_ascii=False)


def triage_ticket(ticket: str, model: MockStructuredModel | None = None) -> TriageDecision:
    """Main application entry point."""

    if not ticket or not ticket.strip():
        raise ValueError("ticket must not be empty")

    model = model or MockStructuredModel()
    raw_output = model.generate(ticket)
    return parse_triage_output(raw_output)


def build_user_reply(decision: TriageDecision) -> str:
    """
    Build a user-facing reply from a validated decision.

    This function deliberately keeps natural language separate from the
    machine-readable structured output.
    """

    if decision.priority in {"high", "critical"}:
        urgency_sentence = "Nous allons traiter cette demande en priorité."
    else:
        urgency_sentence = "Nous allons prendre en charge cette demande."

    return (
        f"{urgency_sentence} "
        f"Votre demande a été transmise à l’équipe {decision.owner_team}. "
        f"Résumé : {decision.summary}"
    )


if __name__ == "__main__":
    sample_ticket = "Je suis très énervé, vous m’avez facturé deux fois ce mois-ci."
    decision = triage_ticket(sample_ticket)

    print("Structured decision:")
    print(json.dumps(decision.__dict__, ensure_ascii=False, indent=2))

    print("\nUser reply:")
    print(build_user_reply(decision))
