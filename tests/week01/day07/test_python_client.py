from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
LAB_PATH = ROOT / "book" / "week01" / "day07" / "labs"
sys.path.insert(0, str(LAB_PATH))

import pytest

from python_client import (
    LLMClient,
    LLMConfig,
    MockTransport,
    StaticTransport,
    LLMValidationError,
)


def test_generate_text_returns_mock_response():
    client = LLMClient(
        config=LLMConfig(model="mock-model"),
        transport=MockTransport(),
    )

    response = client.generate_text("Bonjour")

    assert response.text.startswith("Réponse mock")
    assert response.model == "mock-model"
    assert response.raw["raw"]["mock"] is True


def test_generate_json_returns_dict_when_valid():
    client = LLMClient(
        config=LLMConfig(model="static-model"),
        transport=StaticTransport(
            '{"label": "technical", "confidence": 0.95, "reason": "API Python"}'
        ),
    )

    result = client.generate_json(
        "Classe ce texte.",
        required_fields=["label", "confidence", "reason"],
    )

    assert result["label"] == "technical"
    assert result["confidence"] == 0.95


def test_generate_json_raises_when_field_missing():
    client = LLMClient(
        config=LLMConfig(model="static-model"),
        transport=StaticTransport('{"label": "technical"}'),
    )

    with pytest.raises(LLMValidationError):
        client.generate_json(
            "Classe ce texte.",
            required_fields=["label", "confidence"],
        )


def test_generate_json_raises_when_invalid_json():
    client = LLMClient(
        config=LLMConfig(model="static-model"),
        transport=StaticTransport("pas du json"),
    )

    with pytest.raises(LLMValidationError):
        client.generate_json("Retourne un JSON.", required_fields=["label"])


def test_prompt_cannot_be_empty():
    client = LLMClient(
        config=LLMConfig(model="mock-model"),
        transport=MockTransport(),
    )

    with pytest.raises(LLMValidationError):
        client.generate_text("   ")
