from __future__ import annotations

import json
from typing import Any

from .config import LLMConfig
from .errors import LLMValidationError
from .models import LLMRequest, LLMResponse
from .transports import LLMTransport, MockTransport


class LLMClient:
    """Client applicatif minimal pour interagir avec un LLM."""

    def __init__(
        self,
        config: LLMConfig | None = None,
        transport: LLMTransport | None = None,
    ) -> None:
        self.config = config or LLMConfig()
        self.transport = transport or MockTransport()

    def generate_text(
        self,
        prompt: str,
        user_input: str | None = None,
        *,
        temperature: float | None = None,
        max_output_tokens: int | None = None,
    ) -> LLMResponse:
        if not prompt or not prompt.strip():
            raise LLMValidationError("Le prompt ne peut pas être vide.")

        request = LLMRequest(
            prompt=prompt.strip(),
            user_input=user_input,
            temperature=self.config.temperature if temperature is None else temperature,
            max_output_tokens=(
                self.config.max_output_tokens
                if max_output_tokens is None
                else max_output_tokens
            ),
        )

        raw = self.transport.send(request, self.config)
        text = raw.get("text")
        if not isinstance(text, str) or not text.strip():
            raise LLMValidationError("La réponse texte est vide ou invalide.")

        return LLMResponse(
            text=text,
            model=str(raw.get("model", self.config.model)),
            raw=raw,
        )

    def generate_json(
        self,
        prompt: str,
        required_fields: list[str],
        user_input: str | None = None,
    ) -> dict[str, Any]:
        response = self.generate_text(prompt=prompt, user_input=user_input)

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as exc:
            raise LLMValidationError("La réponse n'est pas un JSON valide.") from exc

        if not isinstance(data, dict):
            raise LLMValidationError("La réponse JSON doit être un objet.")

        missing = [field for field in required_fields if field not in data]
        if missing:
            raise LLMValidationError(f"Champs obligatoires manquants: {missing}")

        return data
