"""
Semaine 3 - Jour 6 - Context Engineering.

Ce module est volontairement autonome et utilise uniquement la Python standard
library. Il illustre comment construire un "context pack" avant un appel modèle.

Le moteur ne contacte aucun LLM. Il prépare le contexte qu'un agent pourrait
ensuite transmettre à un modèle.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Iterable, Literal
import json
import re


ContextKind = Literal[
    "system",
    "goal",
    "state",
    "recent_message",
    "memory",
    "resource",
    "tool",
    "trace",
]

Visibility = Literal["private", "shared", "public"]

DropReason = Literal[
    "kind_excluded",
    "priority_too_low",
    "visibility_not_allowed",
    "wrong_target_agent",
    "duplicate",
    "budget_exceeded",
]


EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(
    r"(?:(?:\+|00)\d{1,3}[\s.-]?)?(?:\(?\d{1,4}\)?[\s.-]?){3,}\d{2,4}"
)


def estimate_tokens(text: str) -> int:
    """Estimate token cost with a deterministic approximation.

    This is not model-accurate. It is good enough for pedagogical budgeting.
    """
    if not text:
        return 0
    words = re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)
    return max(1, int(len(words) * 1.3))


def normalize_content(text: str) -> str:
    """Normalize content for exact deduplication."""
    return " ".join(text.casefold().strip().split())


def redact_pii(text: str) -> str:
    """Redact simple email and phone patterns."""
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = PHONE_RE.sub("[REDACTED_PHONE]", text)
    return text


@dataclass(frozen=True)
class ContextItem:
    """One candidate piece of context.

    Args:
        id: Stable identifier used for tracing.
        kind: Semantic type of context.
        content: Text content that could be rendered for the model.
        priority: Higher values are selected first.
        visibility: Access level.
        source: Origin of the context item.
        target_agents: Optional list of agents allowed or intended to receive it.
        metadata: Optional structured metadata.
    """

    id: str
    kind: ContextKind
    content: str
    priority: int
    visibility: Visibility = "public"
    source: str = "unknown"
    target_agents: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def tokens(self) -> int:
        return estimate_tokens(self.content)

    def for_rendering(self, redact: bool) -> "ContextItem":
        if not redact:
            return self
        return ContextItem(
            id=self.id,
            kind=self.kind,
            content=redact_pii(self.content),
            priority=self.priority,
            visibility=self.visibility,
            source=self.source,
            target_agents=self.target_agents,
            metadata=self.metadata,
        )


@dataclass(frozen=True)
class ContextPolicy:
    """Rules used to build a context pack."""

    max_tokens: int
    allowed_visibilities: tuple[Visibility, ...] = ("public", "shared")
    include_kinds: tuple[ContextKind, ...] = (
        "system",
        "goal",
        "state",
        "recent_message",
        "memory",
        "resource",
        "tool",
    )
    min_priority: int = 0
    redact_sensitive_data: bool = True
    agent_name: str | None = None
    preserve_kinds: tuple[ContextKind, ...] = ("system", "goal", "state")


@dataclass(frozen=True)
class DroppedItem:
    id: str
    reason: DropReason
    tokens: int
    priority: int


@dataclass
class ContextPack:
    """Final context package ready to render."""

    goal: str
    selected: list[ContextItem]
    dropped: list[DroppedItem]
    total_tokens: int
    warnings: list[str] = field(default_factory=list)

    def render(self) -> str:
        """Render selected context in deterministic sections."""
        sections: dict[str, list[ContextItem]] = {}
        for item in self.selected:
            sections.setdefault(item.kind, []).append(item)

        order = [
            "system",
            "goal",
            "state",
            "recent_message",
            "memory",
            "resource",
            "tool",
            "trace",
        ]

        lines = [
            "# Context Pack",
            "",
            f"Goal: {self.goal}",
            f"Estimated tokens: {self.total_tokens}",
            "",
        ]

        for kind in order:
            items = sections.get(kind, [])
            if not items:
                continue
            lines.append(f"## {kind}")
            for item in items:
                lines.append(f"- [{item.id} | source={item.source}] {item.content}")
            lines.append("")

        if self.warnings:
            lines.append("## warnings")
            for warning in self.warnings:
                lines.append(f"- {warning}")

        return "\n".join(lines).strip()

    def to_dict(self) -> dict[str, Any]:
        return {
            "goal": self.goal,
            "selected": [asdict(item) | {"tokens": item.tokens} for item in self.selected],
            "dropped": [asdict(item) for item in self.dropped],
            "total_tokens": self.total_tokens,
            "warnings": list(self.warnings),
        }


class ContextEngineer:
    """Build context packs from candidate context items."""

    def __init__(self, items: Iterable[ContextItem] | None = None):
        self._items: list[ContextItem] = list(items or [])

    def add_item(self, item: ContextItem) -> None:
        if not item.id:
            raise ValueError("ContextItem.id is required")
        if not item.content:
            raise ValueError("ContextItem.content is required")
        if not 0 <= item.priority <= 100:
            raise ValueError("ContextItem.priority must be between 0 and 100")
        self._items.append(item)

    def build(self, goal: str, policy: ContextPolicy) -> ContextPack:
        if policy.max_tokens <= 0:
            raise ValueError("ContextPolicy.max_tokens must be positive")

        selected: list[ContextItem] = []
        dropped: list[DroppedItem] = []
        warnings: list[str] = []
        seen_normalized: set[str] = set()
        total_tokens = 0

        candidates = sorted(
            self._items,
            key=lambda item: (
                item.kind not in policy.preserve_kinds,
                -item.priority,
                item.tokens,
                item.id,
            ),
        )

        for item in candidates:
            reason = self._drop_reason_before_budget(item, policy)
            if reason:
                dropped.append(self._dropped(item, reason))
                continue

            normalized = normalize_content(item.content)
            if normalized in seen_normalized:
                dropped.append(self._dropped(item, "duplicate"))
                continue

            rendered = item.for_rendering(policy.redact_sensitive_data)
            item_tokens = rendered.tokens

            if total_tokens + item_tokens > policy.max_tokens:
                dropped.append(self._dropped(item, "budget_exceeded"))
                if item.kind in policy.preserve_kinds:
                    warnings.append(
                        f"Preserved kind '{item.kind}' could not fit budget: {item.id}"
                    )
                continue

            selected.append(rendered)
            seen_normalized.add(normalized)
            total_tokens += item_tokens

        if not any(item.kind == "system" for item in selected):
            warnings.append("No system instruction selected.")
        if not any(item.kind == "state" for item in selected):
            warnings.append("No task state selected.")

        return ContextPack(
            goal=goal,
            selected=selected,
            dropped=dropped,
            total_tokens=total_tokens,
            warnings=warnings,
        )

    def _drop_reason_before_budget(
        self, item: ContextItem, policy: ContextPolicy
    ) -> DropReason | None:
        if item.kind not in policy.include_kinds:
            return "kind_excluded"
        if item.priority < policy.min_priority:
            return "priority_too_low"
        if item.visibility not in policy.allowed_visibilities:
            return "visibility_not_allowed"
        if policy.agent_name and item.target_agents:
            if policy.agent_name not in item.target_agents:
                return "wrong_target_agent"
        return None

    @staticmethod
    def _dropped(item: ContextItem, reason: DropReason) -> DroppedItem:
        return DroppedItem(
            id=item.id,
            reason=reason,
            tokens=item.tokens,
            priority=item.priority,
        )


def build_demo_items() -> list[ContextItem]:
    """Return a deterministic demo inventory."""
    return [
        ContextItem(
            id="system_support",
            kind="system",
            content="Tu es un agent support interne. Réponds avec les sources autorisées.",
            priority=100,
            visibility="public",
            source="policy",
        ),
        ContextItem(
            id="goal_invoice",
            kind="goal",
            content="Résoudre le blocage de la facture F-392 pour le client ACME.",
            priority=98,
            visibility="public",
            source="user_request",
        ),
        ContextItem(
            id="state_invoice",
            kind="state",
            content="ticket_id=T-204 invoice_id=F-392 customer=ACME status=waiting_for_invoice_status",
            priority=95,
            visibility="shared",
            source="shared_state",
            target_agents=("billing_agent",),
        ),
        ContextItem(
            id="recent_user_message",
            kind="recent_message",
            content="Je n'ai toujours pas reçu de réponse au sujet de la facture.",
            priority=70,
            visibility="public",
            source="conversation",
        ),
        ContextItem(
            id="memory_format",
            kind="memory",
            content="L'utilisateur préfère des réponses structurées avec étapes courtes.",
            priority=45,
            visibility="shared",
            source="long_term_memory",
        ),
        ContextItem(
            id="billing_policy",
            kind="resource",
            content="Politique facturation: vérifier le statut, confirmer l'identifiant, ne jamais supprimer une facture sans validation humaine.",
            priority=80,
            visibility="shared",
            source="mcp://billing/policy",
            target_agents=("billing_agent",),
        ),
        ContextItem(
            id="tool_get_invoice",
            kind="tool",
            content="get_invoice_status(invoice_id: str) -> invoice status and payment blockers",
            priority=85,
            visibility="public",
            source="mcp://billing/tools",
            target_agents=("billing_agent",),
        ),
        ContextItem(
            id="tool_delete_invoice",
            kind="tool",
            content="delete_invoice(invoice_id: str) -> destructive operation requiring approval",
            priority=15,
            visibility="public",
            source="mcp://billing/tools",
            target_agents=("billing_agent",),
        ),
        ContextItem(
            id="private_security_note",
            kind="memory",
            content="Suspicion de secret exposé. Contacter secops@example.com au +33 6 12 34 56 78.",
            priority=90,
            visibility="private",
            source="security_agent",
            target_agents=("security_agent",),
        ),
        ContextItem(
            id="duplicate_recent_message",
            kind="recent_message",
            content=" je n'ai toujours pas reçu de réponse au sujet de la facture. ",
            priority=65,
            visibility="public",
            source="conversation",
        ),
        ContextItem(
            id="old_trace",
            kind="trace",
            content="Ancien run: l'agent a consulté un ticket RH sans rapport.",
            priority=5,
            visibility="shared",
            source="trace_store",
        ),
    ]


def demo() -> ContextPack:
    engine = ContextEngineer(build_demo_items())
    policy = ContextPolicy(
        max_tokens=120,
        allowed_visibilities=("public", "shared"),
        include_kinds=("system", "goal", "state", "recent_message", "memory", "resource", "tool"),
        min_priority=20,
        agent_name="billing_agent",
        redact_sensitive_data=True,
    )
    return engine.build(
        goal="Expliquer pourquoi la facture F-392 est bloquée.",
        policy=policy,
    )


if __name__ == "__main__":
    pack = demo()
    print(pack.render())
    print("\n--- audit ---")
    print(json.dumps(pack.to_dict(), ensure_ascii=False, indent=2))
