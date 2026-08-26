"""
Semaine 2 - Jour 2 : Function Calling

Mini-agent local de support client.

Le fichier est volontairement autonome :
- aucune dépendance externe ;
- aucun appel réseau ;
- aucune clé API ;
- tests possibles avec Python standard.

Exécution :
    python book/week02/day02/labs/function_calling_agent.py
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any, Callable


JsonDict = dict[str, Any]


@dataclass(frozen=True)
class ToolCall:
    """Représente une demande structurée d'appel d'outil."""

    name: str
    arguments: JsonDict


@dataclass(frozen=True)
class ToolSpec:
    """Associe le schéma exposé au modèle et le handler applicatif."""

    schema: JsonDict
    handler: Callable[..., JsonDict]


class ToolCallError(Exception):
    """Erreur contrôlée de function calling."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message

    def to_dict(self) -> JsonDict:
        return {"code": self.code, "message": self.message}


class ToolRegistry:
    """Registre explicite des outils autorisés."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, schema: JsonDict, handler: Callable[..., JsonDict]) -> None:
        name = schema.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("Le schéma d'outil doit contenir un nom non vide.")

        if name in self._tools:
            raise ValueError(f"Outil déjà enregistré: {name}")

        self._tools[name] = ToolSpec(schema=schema, handler=handler)

    def list_schemas(self) -> list[JsonDict]:
        """Retourne uniquement les contrats exposables au modèle."""

        return [tool.schema for tool in self._tools.values()]

    def validate(self, call: ToolCall) -> None:
        """Valide l'existence de l'outil et ses arguments."""

        if call.name not in self._tools:
            raise ToolCallError("UNKNOWN_TOOL", f"Outil inconnu: {call.name}")

        schema = self._tools[call.name].schema
        parameters = schema.get("parameters", {})

        if parameters.get("type") != "object":
            raise ToolCallError("INVALID_SCHEMA", "Le schéma doit être de type object.")

        properties: JsonDict = parameters.get("properties", {})
        required: list[str] = parameters.get("required", [])

        for field in required:
            if field not in call.arguments:
                raise ToolCallError("MISSING_ARGUMENT", f"Argument manquant: {field}")

        if parameters.get("additionalProperties") is False:
            extra_fields = sorted(set(call.arguments) - set(properties))
            if extra_fields:
                raise ToolCallError(
                    "UNEXPECTED_ARGUMENT",
                    f"Arguments non autorisés: {extra_fields}",
                )

        for field, value in call.arguments.items():
            if field not in properties:
                continue

            field_schema = properties[field]
            expected_type = field_schema.get("type")

            if expected_type == "string" and not isinstance(value, str):
                raise ToolCallError("INVALID_ARGUMENT_TYPE", f"{field} doit être une chaîne.")

            allowed_values = field_schema.get("enum")
            if allowed_values is not None and value not in allowed_values:
                raise ToolCallError(
                    "INVALID_ENUM_VALUE",
                    f"{field} doit être dans {allowed_values}. Valeur reçue: {value}",
                )

    def dispatch(self, call: ToolCall) -> JsonDict:
        """Valide puis exécute un appel d'outil."""

        self.validate(call)

        spec = self._tools[call.name]
        started = perf_counter()

        try:
            data = spec.handler(**call.arguments)
            duration_ms = round((perf_counter() - started) * 1000, 3)
            return {
                "ok": True,
                "tool": call.name,
                "data": data,
                "trace": {
                    "tool": call.name,
                    "ok": True,
                    "duration_ms": duration_ms,
                },
            }
        except ToolCallError as exc:
            duration_ms = round((perf_counter() - started) * 1000, 3)
            return {
                "ok": False,
                "tool": call.name,
                "error": exc.to_dict(),
                "trace": {
                    "tool": call.name,
                    "ok": False,
                    "duration_ms": duration_ms,
                },
            }


ORDERS: dict[str, JsonDict] = {
    "ORD-1001": {
        "order_id": "ORD-1001",
        "status": "shipped",
        "carrier": "DHL",
        "eta": "2026-08-12",
        "amount_eur": 129.90,
    },
    "ORD-1002": {
        "order_id": "ORD-1002",
        "status": "processing",
        "carrier": None,
        "eta": "2026-08-15",
        "amount_eur": 59.00,
    },
    "ORD-1003": {
        "order_id": "ORD-1003",
        "status": "delivered",
        "carrier": "Colissimo",
        "eta": "2026-08-07",
        "amount_eur": 219.50,
    },
}


def get_order_status(order_id: str) -> JsonDict:
    """Récupère le statut d'une commande."""

    order = ORDERS.get(order_id)
    if order is None:
        raise ToolCallError("ORDER_NOT_FOUND", f"Aucune commande ne correspond à {order_id}.")

    return {
        "order_id": order["order_id"],
        "status": order["status"],
        "carrier": order["carrier"],
        "eta": order["eta"],
    }


def estimate_refund(order_id: str, reason: str) -> JsonDict:
    """Estime un remboursement simple selon une raison métier."""

    order = ORDERS.get(order_id)
    if order is None:
        raise ToolCallError("ORDER_NOT_FOUND", f"Aucune commande ne correspond à {order_id}.")

    amount = float(order["amount_eur"])
    ratio_by_reason = {
        "damaged": 1.0,
        "late_delivery": 0.25,
        "changed_mind": 0.0,
    }

    ratio = ratio_by_reason.get(reason, 0.0)
    return {
        "order_id": order_id,
        "reason": reason,
        "estimated_refund_eur": round(amount * ratio, 2),
        "requires_human_review": ratio == 1.0,
    }


def create_support_ticket(order_id: str, issue: str, priority: str) -> JsonDict:
    """Crée un ticket de support fictif."""

    if order_id not in ORDERS:
        raise ToolCallError("ORDER_NOT_FOUND", f"Aucune commande ne correspond à {order_id}.")

    ticket_id = f"TCK-{order_id.split('-')[-1]}"
    return {
        "ticket_id": ticket_id,
        "order_id": order_id,
        "issue": issue,
        "priority": priority,
        "status": "created",
    }


GET_ORDER_STATUS_SCHEMA: JsonDict = {
    "name": "get_order_status",
    "description": "Récupère le statut logistique d'une commande client.",
    "parameters": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "Identifiant de commande, par exemple ORD-1001.",
            }
        },
        "required": ["order_id"],
        "additionalProperties": False,
    },
}


ESTIMATE_REFUND_SCHEMA: JsonDict = {
    "name": "estimate_refund",
    "description": "Estime le remboursement potentiel d'une commande selon une raison déclarée.",
    "parameters": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "Identifiant de commande, par exemple ORD-1001.",
            },
            "reason": {
                "type": "string",
                "enum": ["damaged", "late_delivery", "changed_mind"],
                "description": "Motif de remboursement.",
            },
        },
        "required": ["order_id", "reason"],
        "additionalProperties": False,
    },
}


CREATE_SUPPORT_TICKET_SCHEMA: JsonDict = {
    "name": "create_support_ticket",
    "description": "Crée un ticket de support pour une commande existante.",
    "parameters": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "Identifiant de commande, par exemple ORD-1001.",
            },
            "issue": {
                "type": "string",
                "description": "Résumé court du problème client.",
            },
            "priority": {
                "type": "string",
                "enum": ["low", "normal", "high"],
                "description": "Priorité du ticket.",
            },
        },
        "required": ["order_id", "issue", "priority"],
        "additionalProperties": False,
    },
}


class FakePlanner:
    """
    Planificateur déterministe qui remplace un LLM pour le lab.

    Dans une intégration réelle, cette classe serait remplacée par un appel à un
    modèle recevant le message utilisateur et la liste des outils disponibles.
    """

    def plan(self, user_message: str, available_tools: list[JsonDict]) -> ToolCall:
        del available_tools  # Le lab garde l'interface réaliste sans utiliser cette variable.

        message = user_message.lower()

        if "outil inconnu" in message:
            return ToolCall(name="delete_everything", arguments={})

        if "argument extra" in message:
            return ToolCall(
                name="get_order_status",
                arguments={"order_id": "ORD-1001", "debug": "true"},
            )

        if "priorité invalide" in message or "priority invalide" in message:
            return ToolCall(
                name="create_support_ticket",
                arguments={
                    "order_id": "ORD-1001",
                    "issue": "Le colis est arrivé abîmé.",
                    "priority": "urgent",
                },
            )

        if "remboursement" in message or "refund" in message:
            return ToolCall(
                name="estimate_refund",
                arguments={"order_id": extract_order_id(user_message), "reason": "damaged"},
            )

        if "ticket" in message or "support" in message:
            return ToolCall(
                name="create_support_ticket",
                arguments={
                    "order_id": extract_order_id(user_message),
                    "issue": "Demande de support client.",
                    "priority": "normal",
                },
            )

        return ToolCall(
            name="get_order_status",
            arguments={"order_id": extract_order_id(user_message)},
        )


def extract_order_id(text: str) -> str:
    """Extrait un identifiant de commande simple depuis un message."""

    for token in text.replace("?", " ").replace(".", " ").split():
        cleaned = token.strip().upper()
        if cleaned.startswith("ORD-"):
            return cleaned

    return "ORD-1001"


class SupportAgent:
    """Agent mono-agent minimal utilisant un registre d'outils."""

    def __init__(self, registry: ToolRegistry, planner: FakePlanner) -> None:
        self.registry = registry
        self.planner = planner

    def run(self, user_message: str) -> JsonDict:
        tool_call = self.planner.plan(user_message, self.registry.list_schemas())

        try:
            tool_result = self.registry.dispatch(tool_call)
        except ToolCallError as exc:
            return {
                "ok": False,
                "message": "Je ne peux pas exécuter cette action.",
                "error": exc.to_dict(),
            }

        if not tool_result["ok"]:
            return {
                "ok": False,
                "message": "L'outil a retourné une erreur contrôlée.",
                "tool_result": tool_result,
            }

        return {
            "ok": True,
            "message": render_user_message(tool_call.name, tool_result["data"]),
            "tool_result": tool_result,
        }


def render_user_message(tool_name: str, data: JsonDict) -> str:
    """Transforme un résultat d'outil en réponse utilisateur."""

    if tool_name == "get_order_status":
        carrier = data["carrier"] or "transporteur non encore assigné"
        return (
            f"La commande {data['order_id']} est {data['status']}. "
            f"Transporteur: {carrier}. ETA: {data['eta']}."
        )

    if tool_name == "estimate_refund":
        return (
            f"Le remboursement estimé pour {data['order_id']} est de "
            f"{data['estimated_refund_eur']} EUR."
        )

    if tool_name == "create_support_ticket":
        return (
            f"Le ticket {data['ticket_id']} a été créé avec la priorité "
            f"{data['priority']}."
        )

    return "Action exécutée."


def build_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(GET_ORDER_STATUS_SCHEMA, get_order_status)
    registry.register(ESTIMATE_REFUND_SCHEMA, estimate_refund)
    registry.register(CREATE_SUPPORT_TICKET_SCHEMA, create_support_ticket)
    return registry


def demo() -> None:
    agent = SupportAgent(registry=build_registry(), planner=FakePlanner())

    messages = [
        "Quel est le statut de la commande ORD-1001 ?",
        "Peux-tu estimer le remboursement pour ORD-1003 ?",
        "Crée un ticket support pour ORD-1002.",
        "Déclenche un outil inconnu.",
        "Teste un argument extra.",
        "Crée un ticket avec priorité invalide.",
    ]

    for message in messages:
        print("\nUSER:", message)
        print("AGENT:", agent.run(message))


if __name__ == "__main__":
    demo()
