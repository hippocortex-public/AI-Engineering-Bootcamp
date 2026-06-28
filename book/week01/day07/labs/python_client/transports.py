from __future__ import annotations

from typing import Protocol, Any
import json

from .config import LLMConfig
from .models import LLMRequest


class LLMTransport(Protocol):
    """Interface minimale pour envoyer une requête LLM."""

    def send(self, request: LLMRequest, config: LLMConfig) -> dict[str, Any]:
        ...


class MockTransport:
    """Transport déterministe pour les tests et démonstrations."""

    def send(self, request: LLMRequest, config: LLMConfig) -> dict[str, Any]:
        text = (
            "Réponse mock: "
            f"prompt='{request.prompt[:40]}', "
            f"user_input='{(request.user_input or '')[:40]}'"
        )
        return {
            "text": text,
            "model": config.model,
            "raw": {"mock": True, "request": request.__dict__},
        }


class StaticTransport:
    """Transport qui retourne toujours le même texte."""

    def __init__(self, text: str, model: str = "static-model") -> None:
        self.text = text
        self.model = model

    def send(self, request: LLMRequest, config: LLMConfig) -> dict[str, Any]:
        return {
            "text": self.text,
            "model": self.model,
            "raw": {"static": True, "request": request.__dict__},
        }


class OpenAIResponsesTransport:
    """
    Transport optionnel basé sur le SDK OpenAI.

    Il n'est utilisé que si le package `openai` est installé et si une clé API
    est disponible. Les tests du bootcamp n'appellent jamais ce transport.
    """

    def send(self, request: LLMRequest, config: LLMConfig) -> dict[str, Any]:
        config.validate_for_real_transport()

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "Le package openai est requis pour OpenAIResponsesTransport."
            ) from exc

        client = OpenAI(api_key=config.api_key, timeout=config.timeout_seconds)
        input_text = request.prompt
        if request.user_input:
            input_text = f"{request.prompt}\n\nEntrée utilisateur:\n{request.user_input}"

        response = client.responses.create(
            model=config.model,
            input=input_text,
            temperature=request.temperature,
            max_output_tokens=request.max_output_tokens,
        )

        text = getattr(response, "output_text", None)
        if text is None:
            # Fallback prudent pour certains objets SDK.
            text = json.dumps(response.model_dump(), ensure_ascii=False)

        return {
            "text": text,
            "model": config.model,
            "raw": response.model_dump() if hasattr(response, "model_dump") else {},
        }
