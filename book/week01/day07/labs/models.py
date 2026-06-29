from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class LLMRequest:
    prompt: str
    user_input: str | None = None
    temperature: float = 0.2
    max_output_tokens: int = 500


@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    raw: dict[str, Any] = field(default_factory=dict)
