from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class LLMConfig:
    """Configuration minimale d'un client LLM."""

    model: str = "gpt-5.5"
    temperature: float = 0.2
    max_output_tokens: int = 500
    timeout_seconds: float = 30.0
    api_key: str | None = None

    @classmethod
    def from_env(cls) -> "LLMConfig":
        """Construit la configuration depuis l'environnement."""
        return cls(api_key=os.getenv("OPENAI_API_KEY"))

    def validate_for_real_transport(self) -> None:
        from .errors import LLMConfigurationError

        if not self.api_key:
            raise LLMConfigurationError(
                "OPENAI_API_KEY est requis pour utiliser le transport réel."
            )
        if not self.model:
            raise LLMConfigurationError("Le modèle ne peut pas être vide.")
        if self.timeout_seconds <= 0:
            raise LLMConfigurationError("Le timeout doit être positif.")
