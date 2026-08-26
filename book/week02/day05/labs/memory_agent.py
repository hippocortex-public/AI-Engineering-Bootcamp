"""
Semaine 2 — Jour 5 : Memory courte, longue et state.

Ce module implémente un agent de support mémoire-aware sans appel réseau.
Il sert à tester les choix d'architecture autour de la mémoire d'agent.

Exécution :
    python memory_agent.py
    python test_memory_agent.py
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any
import json
import re


@dataclass
class Message:
    """Un message court utilisé pour la mémoire de conversation récente."""

    role: str
    content: str


@dataclass
class ShortTermMemory:
    """Historique court borné à quelques messages."""

    max_messages: int = 6
    messages: list[Message] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        """Ajoute un message et tronque l'historique si nécessaire."""
        if role not in {"user", "assistant", "tool"}:
            raise ValueError(f"Unsupported role: {role}")

        cleaned = content.strip()
        if not cleaned:
            return

        self.messages.append(Message(role=role, content=cleaned))

        overflow = len(self.messages) - self.max_messages
        if overflow > 0:
            del self.messages[:overflow]

    def recent(self) -> list[dict[str, str]]:
        """Retourne l'historique récent sous forme sérialisable."""
        return [asdict(message) for message in self.messages]

    def summary(self) -> str:
        """Produit un résumé déterministe très court pour le lab."""
        if not self.messages:
            return "Aucun échange récent."

        last_messages = self.messages[-3:]
        parts = [f"{message.role}: {message.content}" for message in last_messages]
        return " | ".join(parts)


@dataclass
class ConversationState:
    """État de la tâche en cours."""

    intent: str | None = None
    slots: dict[str, str] = field(default_factory=dict)
    missing_slots: list[str] = field(default_factory=list)
    status: str = "idle"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class UserProfile:
    """Mémoire longue minimale d'un utilisateur."""

    user_id: str
    display_name: str | None = None
    preferences: dict[str, str] = field(default_factory=dict)
    facts: list[str] = field(default_factory=list)
    updated_at: str | None = None

    def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class LongTermMemoryStore:
    """Stockage en mémoire vive, isolé par user_id."""

    def __init__(self) -> None:
        self._profiles: dict[str, UserProfile] = {}

    def get_profile(self, user_id: str) -> UserProfile:
        if not user_id:
            raise ValueError("user_id is required")

        if user_id not in self._profiles:
            self._profiles[user_id] = UserProfile(user_id=user_id)
        return self._profiles[user_id]

    def set_display_name(self, user_id: str, display_name: str) -> None:
        profile = self.get_profile(user_id)
        profile.display_name = display_name.strip()
        profile.touch()

    def set_preference(self, user_id: str, key: str, value: str) -> None:
        profile = self.get_profile(user_id)
        profile.preferences[key] = value.strip()
        profile.touch()

    def add_fact(self, user_id: str, fact: str) -> None:
        profile = self.get_profile(user_id)
        cleaned = fact.strip()
        if cleaned and cleaned not in profile.facts:
            profile.facts.append(cleaned)
            profile.touch()

    def forget_user(self, user_id: str) -> None:
        self._profiles.pop(user_id, None)

    def to_json(self) -> str:
        payload = {
            user_id: profile.to_dict()
            for user_id, profile in sorted(self._profiles.items())
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, raw: str) -> "LongTermMemoryStore":
        data = json.loads(raw)
        store = cls()
        for user_id, payload in data.items():
            store._profiles[user_id] = UserProfile(**payload)
        return store


class MemoryAwareSupportAgent:
    """Agent de support déterministe utilisé pour entraîner l'architecture mémoire."""

    PRODUCT_PATTERNS = {
        "billing": "Billing API",
        "paiement": "Billing API",
        "facturation": "Billing API",
        "auth": "Auth API",
        "login": "Auth API",
        "connexion": "Auth API",
        "webhook": "Webhook Service",
    }

    def __init__(self, short_term_max_messages: int = 6) -> None:
        self.memory = LongTermMemoryStore()
        self.short_terms: dict[str, ShortTermMemory] = {}
        self.states: dict[str, ConversationState] = {}
        self.short_term_max_messages = short_term_max_messages

    def receive(self, user_id: str, message: str) -> str:
        """Traite un message utilisateur et retourne une réponse déterministe."""
        if not user_id:
            raise ValueError("user_id is required")

        text = message.strip()
        if not text:
            return "Je n'ai pas reçu de message exploitable."

        short_term = self._short_term_for(user_id)
        state = self._state_for(user_id)

        short_term.add("user", text)
        self._extract_long_term_memory(user_id, text)
        self._update_state(state, text)

        response = self._build_response(user_id, state)
        short_term.add("assistant", response)
        return response

    def build_context(self, user_id: str) -> dict[str, Any]:
        """Construit le contexte minimal à fournir à un modèle."""
        profile = self.memory.get_profile(user_id)
        state = self._state_for(user_id)
        short_term = self._short_term_for(user_id)

        return {
            "profile": profile.to_dict(),
            "state": state.to_dict(),
            "recent_messages": short_term.recent(),
            "short_summary": short_term.summary(),
        }

    def forget_user(self, user_id: str) -> None:
        """Supprime la mémoire longue, la mémoire courte et le state d'un utilisateur."""
        self.memory.forget_user(user_id)
        self.short_terms.pop(user_id, None)
        self.states.pop(user_id, None)

    def clear_current_state(self, user_id: str) -> None:
        """Réinitialise seulement la tâche active."""
        self.states.pop(user_id, None)

    def _short_term_for(self, user_id: str) -> ShortTermMemory:
        if user_id not in self.short_terms:
            self.short_terms[user_id] = ShortTermMemory(
                max_messages=self.short_term_max_messages
            )
        return self.short_terms[user_id]

    def _state_for(self, user_id: str) -> ConversationState:
        if user_id not in self.states:
            self.states[user_id] = ConversationState()
        return self.states[user_id]

    def _extract_long_term_memory(self, user_id: str, text: str) -> None:
        """Extraction déterministe de préférences explicites.

        Dans un système avec LLM, cette étape serait typiquement produite par
        Structured Outputs, puis validée par une MemoryPolicy.
        """
        lowered = text.lower()

        name_match = re.search(
            r"(?:appeler|appelle-moi|m'appeler)\s+([A-ZÀ-Ÿa-zà-ÿ][A-ZÀ-Ÿa-zà-ÿ\-]{1,30})",
            text,
            flags=re.IGNORECASE,
        )
        if name_match:
            self.memory.set_display_name(user_id, name_match.group(1))

        if "je préfère" in lowered or "je prefere" in lowered:
            if "python" in lowered:
                self.memory.set_preference(user_id, "language", "Python")
            if "typescript" in lowered or "type script" in lowered:
                self.memory.set_preference(user_id, "language", "TypeScript")
            if "réponses courtes" in lowered or "reponses courtes" in lowered or "court" in lowered:
                self.memory.set_preference(user_id, "answer_style", "concise")
            if "exemples" in lowered:
                self.memory.set_preference(user_id, "example_preference", "examples")

        if "je travaille" in lowered and "fastapi" in lowered:
            self.memory.add_fact(user_id, "Travaille principalement avec FastAPI")

    def _update_state(self, state: ConversationState, text: str) -> None:
        lowered = text.lower()

        if any(keyword in lowered for keyword in ["problème", "probleme", "ticket", "bug", "erreur", "500", "404"]):
            state.intent = "create_support_ticket"
            state.status = "collecting"

        for pattern, product in self.PRODUCT_PATTERNS.items():
            if pattern in lowered:
                state.slots["product"] = product

        if any(keyword in lowered for keyword in ["500", "404", "timeout", "échoue", "echoue", "erreur"]):
            state.slots["description"] = text

        required = []
        if state.intent == "create_support_ticket":
            for slot in ["product", "description"]:
                if slot not in state.slots:
                    required.append(slot)

        state.missing_slots = required
        if state.intent and not required:
            state.status = "ready"

    def _build_response(self, user_id: str, state: ConversationState) -> str:
        profile = self.memory.get_profile(user_id)
        greeting = f"{profile.display_name}, " if profile.display_name else ""

        language = profile.preferences.get("language")
        style = profile.preferences.get("answer_style")

        personalization = []
        if language:
            personalization.append(f"je peux formuler les exemples en {language}")
        if style == "concise":
            personalization.append("je vais rester concis")

        personalization_text = ""
        if personalization:
            personalization_text = " (" + " et ".join(personalization) + ")"

        if state.intent == "create_support_ticket":
            if state.missing_slots:
                missing = ", ".join(state.missing_slots)
                return f"{greeting}il me manque ces informations pour créer le ticket : {missing}.{personalization_text}"

            return f"{greeting}j'ai les informations nécessaires pour préparer le ticket.{personalization_text}"

        return f"{greeting}je peux vous aider à créer un ticket ou diagnostiquer un problème.{personalization_text}"


def demo() -> None:
    agent = MemoryAwareSupportAgent(short_term_max_messages=4)
    print(agent.receive("user_1", "Tu peux m'appeler Nadia."))
    print(agent.receive("user_1", "Je préfère les exemples en Python et les réponses courtes."))
    print(agent.receive("user_1", "J'ai un problème avec Billing API."))
    print(json.dumps(agent.build_context("user_1"), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    demo()
