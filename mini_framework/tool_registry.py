"""
Semaine 4 — Jour 3
Composant : Tool Registry

Objectif :
Construire un registre d'outils testable pour un mini-framework d'agents.

Le module reste volontairement indépendant d'un fournisseur LLM. Il fournit :
- un contrat de tool ;
- une validation d'arguments ;
- une politique d'accès minimale ;
- une exécution contrôlée ;
- des résultats sérialisables ;
- des traces utiles pour debug et observabilité.

Exécution depuis la racine du projet :
    python book/week04/day03/labs/tool_registry_lab.py
    python book/week04/day03/labs/test_tool_registry.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional
import inspect
import json
import time


JsonDict = Dict[str, Any]
ToolHandler = Callable[[JsonDict, "ToolContext"], Any]

SUPPORTED_TYPES = {"string", "integer", "number", "boolean", "object", "array"}


class ToolRegistryError(Exception):
    """Erreur racine du registre d'outils."""


class ToolSchemaError(ToolRegistryError):
    """Erreur de schéma ou d'arguments."""


class ToolExecutionError(ToolRegistryError):
    """Erreur contrôlée pendant l'exécution d'un outil."""


@dataclass(frozen=True)
class ToolContext:
    """Contexte transmis à chaque tool au moment de l'exécution."""

    user_id: str
    session_id: str
    scopes: frozenset[str] = field(default_factory=frozenset)
    approvals: frozenset[str] = field(default_factory=frozenset)
    metadata: JsonDict = field(default_factory=dict)

    def has_scope(self, scope: Optional[str]) -> bool:
        return scope is None or scope in self.scopes

    def has_approval(self, tool_name: str) -> bool:
        return tool_name in self.approvals or "*" in self.approvals

    def to_dict(self) -> JsonDict:
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "scopes": sorted(self.scopes),
            "approvals": sorted(self.approvals),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class ToolDefinition:
    """Contrat public d'un outil."""

    name: str
    description: str
    input_schema: JsonDict
    output_schema: JsonDict = field(default_factory=lambda: {"type": "object"})
    sensitive: bool = False
    required_scope: Optional[str] = None
    enabled: bool = True
    tags: tuple[str, ...] = field(default_factory=tuple)
    metadata: JsonDict = field(default_factory=dict)

    def public_schema(self) -> JsonDict:
        """Retourne une version sérialisable sans handler Python."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "sensitive": self.sensitive,
            "required_scope": self.required_scope,
            "enabled": self.enabled,
            "tags": list(self.tags),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class ToolResult:
    """Résultat normalisé d'un appel d'outil."""

    tool_name: str
    status: str
    output: Any = None
    error: Optional[str] = None
    elapsed_ms: int = 0
    trace: tuple[JsonDict, ...] = field(default_factory=tuple)

    def to_dict(self) -> JsonDict:
        return {
            "tool_name": self.tool_name,
            "status": self.status,
            "output": self.output,
            "error": self.error,
            "elapsed_ms": self.elapsed_ms,
            "trace": list(self.trace),
        }


@dataclass
class RegisteredTool:
    """Association interne entre contrat et fonction Python."""

    definition: ToolDefinition
    handler: ToolHandler


def now_ms() -> int:
    return int(time.time() * 1000)


def trace_event(step: str, message: str, **metadata: Any) -> JsonDict:
    event = {"step": step, "message": message, "timestamp_ms": now_ms()}
    if metadata:
        event["metadata"] = metadata
    return event


def validate_tool_name(name: str) -> None:
    if not isinstance(name, str) or not name.strip():
        raise ToolSchemaError("Le nom de l'outil est obligatoire.")
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-")
    if any(char not in allowed for char in name):
        raise ToolSchemaError(
            "Le nom d'un outil doit contenir seulement lettres, chiffres, '-' ou '_'."
        )


def validate_schema(schema: JsonDict) -> None:
    """Valide un sous-ensemble pédagogique de JSON Schema."""
    if not isinstance(schema, dict):
        raise ToolSchemaError("Le schéma doit être un dictionnaire.")

    if schema.get("type") != "object":
        raise ToolSchemaError("Le schéma d'entrée racine doit être de type object.")

    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        raise ToolSchemaError("schema.properties doit être un dictionnaire.")

    required = schema.get("required", [])
    if not isinstance(required, list):
        raise ToolSchemaError("schema.required doit être une liste.")

    for field_name in required:
        if field_name not in properties:
            raise ToolSchemaError(f"Champ requis absent de properties: {field_name}")

    for field_name, spec in properties.items():
        if not isinstance(spec, dict):
            raise ToolSchemaError(f"Le champ {field_name} doit avoir un schéma.")
        field_type = spec.get("type")
        if field_type not in SUPPORTED_TYPES:
            raise ToolSchemaError(f"Type non supporté pour {field_name}: {field_type}")
        if "enum" in spec and not isinstance(spec["enum"], list):
            raise ToolSchemaError(f"enum doit être une liste pour {field_name}.")


def _matches_type(value: Any, expected_type: str) -> bool:
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "number":
        return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    return False


def validate_arguments(schema: JsonDict, arguments: JsonDict) -> JsonDict:
    """Valide et normalise des arguments selon le sous-ensemble supporté."""
    validate_schema(schema)

    if not isinstance(arguments, dict):
        raise ToolSchemaError("Les arguments doivent être un dictionnaire.")

    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    additional_allowed = schema.get("additionalProperties", True)

    missing = sorted(required - set(arguments))
    if missing:
        raise ToolSchemaError(f"Champs requis manquants: {', '.join(missing)}")

    if additional_allowed is False:
        extra = sorted(set(arguments) - set(properties))
        if extra:
            raise ToolSchemaError(f"Champs inattendus: {', '.join(extra)}")

    normalized = dict(arguments)

    for field_name, spec in properties.items():
        if field_name not in normalized:
            if "default" in spec:
                normalized[field_name] = spec["default"]
            continue

        value = normalized[field_name]
        expected_type = spec["type"]
        if not _matches_type(value, expected_type):
            raise ToolSchemaError(
                f"Type invalide pour {field_name}: attendu {expected_type}, reçu {type(value).__name__}"
            )

        if "enum" in spec and value not in spec["enum"]:
            allowed = ", ".join(str(item) for item in spec["enum"])
            raise ToolSchemaError(f"Valeur invalide pour {field_name}: {value}. Valeurs: {allowed}")

    return normalized


class ToolRegistry:
    """Registre d'outils d'un agent ou d'un workflow."""

    def __init__(self) -> None:
        self._tools: Dict[str, RegisteredTool] = {}

    def register(
        self,
        name: str,
        description: str,
        input_schema: JsonDict,
        handler: ToolHandler,
        *,
        output_schema: Optional[JsonDict] = None,
        sensitive: bool = False,
        required_scope: Optional[str] = None,
        enabled: bool = True,
        tags: Optional[Iterable[str]] = None,
        metadata: Optional[JsonDict] = None,
    ) -> "ToolRegistry":
        validate_tool_name(name)
        validate_schema(input_schema)

        if name in self._tools:
            raise ToolSchemaError(f"Outil déjà enregistré: {name}")
        if not callable(handler):
            raise ToolSchemaError("handler doit être callable.")
        if not description.strip():
            raise ToolSchemaError("description est obligatoire.")

        definition = ToolDefinition(
            name=name,
            description=description,
            input_schema=dict(input_schema),
            output_schema=output_schema or {"type": "object"},
            sensitive=sensitive,
            required_scope=required_scope,
            enabled=enabled,
            tags=tuple(tags or ()),
            metadata=dict(metadata or {}),
        )
        self._tools[name] = RegisteredTool(definition=definition, handler=handler)
        return self

    def unregister(self, name: str) -> None:
        if name not in self._tools:
            raise ToolRegistryError(f"Outil inconnu: {name}")
        del self._tools[name]

    def has(self, name: str) -> bool:
        return name in self._tools

    def get(self, name: str) -> ToolDefinition:
        try:
            return self._tools[name].definition
        except KeyError as exc:
            raise ToolRegistryError(f"Outil inconnu: {name}") from exc

    def list_tools(
        self,
        *,
        include_sensitive: bool = False,
        enabled_only: bool = True,
        tag: Optional[str] = None,
    ) -> List[JsonDict]:
        items: List[JsonDict] = []
        for registered in self._tools.values():
            definition = registered.definition
            if enabled_only and not definition.enabled:
                continue
            if definition.sensitive and not include_sensitive:
                continue
            if tag is not None and tag not in definition.tags:
                continue
            items.append(definition.public_schema())
        return sorted(items, key=lambda item: item["name"])

    def export_manifest(self) -> JsonDict:
        return {
            "tool_count": len(self._tools),
            "tools": self.list_tools(include_sensitive=True, enabled_only=False),
        }

    def call(self, name: str, arguments: JsonDict, context: ToolContext) -> ToolResult:
        trace: List[JsonDict] = [trace_event("registry.lookup", f"Recherche de l'outil {name}")]
        started = time.perf_counter()

        if name not in self._tools:
            elapsed = int((time.perf_counter() - started) * 1000)
            trace.append(trace_event("registry.error", "Outil inconnu"))
            return ToolResult(name, "failed", error=f"Outil inconnu: {name}", elapsed_ms=elapsed, trace=tuple(trace))

        registered = self._tools[name]
        definition = registered.definition

        if not definition.enabled:
            elapsed = int((time.perf_counter() - started) * 1000)
            trace.append(trace_event("policy.blocked", "Outil désactivé"))
            return ToolResult(name, "blocked", error=f"Outil désactivé: {name}", elapsed_ms=elapsed, trace=tuple(trace))

        if not context.has_scope(definition.required_scope):
            elapsed = int((time.perf_counter() - started) * 1000)
            trace.append(trace_event("policy.blocked", "Scope manquant", required_scope=definition.required_scope))
            return ToolResult(
                name,
                "blocked",
                error=f"Scope requis manquant: {definition.required_scope}",
                elapsed_ms=elapsed,
                trace=tuple(trace),
            )

        if definition.sensitive and not context.has_approval(name):
            elapsed = int((time.perf_counter() - started) * 1000)
            trace.append(trace_event("policy.blocked", "Approbation humaine requise"))
            return ToolResult(
                name,
                "blocked",
                error=f"Approbation humaine requise pour l'outil sensible: {name}",
                elapsed_ms=elapsed,
                trace=tuple(trace),
            )

        try:
            trace.append(trace_event("schema.validate", "Validation des arguments"))
            normalized_arguments = validate_arguments(definition.input_schema, arguments)
            trace.append(trace_event("tool.execute", "Exécution du handler"))
            output = registered.handler(normalized_arguments, context)
            elapsed = int((time.perf_counter() - started) * 1000)
            trace.append(trace_event("tool.completed", "Outil terminé", elapsed_ms=elapsed))
            return ToolResult(name, "completed", output=output, elapsed_ms=elapsed, trace=tuple(trace))
        except ToolRegistryError as exc:
            elapsed = int((time.perf_counter() - started) * 1000)
            trace.append(trace_event("tool.failed", str(exc)))
            return ToolResult(name, "failed", error=str(exc), elapsed_ms=elapsed, trace=tuple(trace))
        except Exception as exc:
            elapsed = int((time.perf_counter() - started) * 1000)
            trace.append(trace_event("tool.failed", "Exception non contrôlée capturée"))
            return ToolResult(name, "failed", error=f"Erreur d'exécution: {exc}", elapsed_ms=elapsed, trace=tuple(trace))


def type_to_schema(annotation: Any) -> str:
    """Convertit quelques annotations Python simples en types JSON Schema.

    Les notebooks et les fichiers avec ``from __future__ import annotations``
    peuvent fournir les annotations sous forme de chaînes. Le mapping accepte
    donc les objets Python et leurs représentations textuelles courantes.
    """
    if annotation is inspect.Signature.empty:
        return "string"

    normalized = annotation
    if isinstance(annotation, str):
        normalized = annotation.lower()

    if normalized is str or normalized in {"str", "string"}:
        return "string"
    if normalized is int or normalized in {"int", "integer"}:
        return "integer"
    if normalized is float or normalized in {"float", "number"}:
        return "number"
    if normalized is bool or normalized in {"bool", "boolean"}:
        return "boolean"
    if normalized is dict or normalized in {"dict", "object"}:
        return "object"
    if normalized is list or normalized in {"list", "array"}:
        return "array"
    return "string"


def schema_from_function(func: Callable[..., Any]) -> JsonDict:
    signature = inspect.signature(func)
    properties: JsonDict = {}
    required: List[str] = []

    for name, parameter in signature.parameters.items():
        if name in {"context", "ctx"}:
            continue
        properties[name] = {
            "type": type_to_schema(parameter.annotation),
            "description": f"Paramètre {name}",
        }
        if parameter.default is inspect.Signature.empty:
            required.append(name)
        else:
            properties[name]["default"] = parameter.default

    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


def tool(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    sensitive: bool = False,
    required_scope: Optional[str] = None,
    tags: Optional[Iterable[str]] = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Décorateur pédagogique qui ajoute un contrat de tool à une fonction."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        tool_name = name or func.__name__
        tool_description = description or inspect.getdoc(func) or f"Outil {tool_name}"
        input_schema = schema_from_function(func)

        def handler(arguments: JsonDict, context: ToolContext) -> Any:
            accepted = inspect.signature(func).parameters
            kwargs = {key: value for key, value in arguments.items() if key in accepted}
            if "context" in accepted:
                kwargs["context"] = context
            elif "ctx" in accepted:
                kwargs["ctx"] = context
            return func(**kwargs)

        setattr(handler, "_tool_definition", {
            "name": tool_name,
            "description": tool_description,
            "input_schema": input_schema,
            "sensitive": sensitive,
            "required_scope": required_scope,
            "tags": tuple(tags or ()),
        })
        setattr(handler, "__wrapped__", func)
        return handler

    return decorator


def register_decorated(registry: ToolRegistry, decorated_handler: ToolHandler) -> ToolRegistry:
    definition = getattr(decorated_handler, "_tool_definition", None)
    if definition is None:
        raise ToolSchemaError("La fonction n'a pas été décorée avec @tool.")
    return registry.register(
        definition["name"],
        definition["description"],
        definition["input_schema"],
        decorated_handler,
        sensitive=definition["sensitive"],
        required_scope=definition["required_scope"],
        tags=definition["tags"],
    )


def build_demo_registry() -> ToolRegistry:
    """Construit un registre d'exemple réutilisé par le lab et les tests."""
    registry = ToolRegistry()

    def add_numbers(arguments: JsonDict, context: ToolContext) -> JsonDict:
        return {
            "sum": arguments["a"] + arguments["b"],
            "session_id": context.session_id,
        }

    def search_policy(arguments: JsonDict, context: ToolContext) -> JsonDict:
        corpus = {
            "refund": "Les remboursements standard sont possibles sous 30 jours.",
            "security": "Toute action sensible requiert une approbation humaine.",
            "sla": "Le SLA support premium cible une réponse en moins de 4 heures.",
        }
        query = arguments["query"].lower()
        matches = [text for key, text in corpus.items() if key in query or query in key]
        return {"matches": matches, "count": len(matches)}

    def create_ticket(arguments: JsonDict, context: ToolContext) -> JsonDict:
        return {
            "ticket_id": f"TICKET-{context.session_id.upper()}-001",
            "priority": arguments["priority"],
            "title": arguments["title"],
        }

    def fail_tool(arguments: JsonDict, context: ToolContext) -> JsonDict:
        raise RuntimeError("service indisponible")

    registry.register(
        "add_numbers",
        "Additionne deux nombres entiers.",
        {
            "type": "object",
            "properties": {
                "a": {"type": "integer", "description": "Premier entier"},
                "b": {"type": "integer", "description": "Second entier"},
            },
            "required": ["a", "b"],
            "additionalProperties": False,
        },
        add_numbers,
        tags=["math", "safe"],
    )

    registry.register(
        "search_policy",
        "Recherche une politique interne dans un corpus pédagogique.",
        {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Terme recherché"},
                "limit": {"type": "integer", "description": "Nombre maximum de résultats", "default": 3},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
        search_policy,
        required_scope="policy:read",
        tags=["knowledge", "safe"],
    )

    registry.register(
        "create_ticket",
        "Crée un ticket de support. Action sensible.",
        {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Titre du ticket"},
                "priority": {
                    "type": "string",
                    "description": "Priorité",
                    "enum": ["low", "medium", "high"],
                    "default": "medium",
                },
            },
            "required": ["title"],
            "additionalProperties": False,
        },
        create_ticket,
        sensitive=True,
        required_scope="ticket:write",
        tags=["support", "sensitive"],
    )

    registry.register(
        "disabled_tool",
        "Outil volontairement désactivé.",
        {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        lambda arguments, context: {"ok": True},
        enabled=False,
        tags=["internal"],
    )

    registry.register(
        "fail_tool",
        "Outil qui échoue pour tester la gestion d'erreur.",
        {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        fail_tool,
        tags=["debug"],
    )

    return registry


if __name__ == "__main__":
    demo = build_demo_registry()
    ctx = ToolContext(
        user_id="user_123",
        session_id="session_abc",
        scopes=frozenset({"policy:read", "ticket:write"}),
        approvals=frozenset({"create_ticket"}),
    )

    print(json.dumps(demo.export_manifest(), indent=2, ensure_ascii=False))
    result = demo.call("add_numbers", {"a": 2, "b": 40}, ctx)
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
