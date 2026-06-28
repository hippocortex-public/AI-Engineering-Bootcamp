from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
LAB_PATH = ROOT / "book" / "week01" / "day07" / "labs"
sys.path.insert(0, str(LAB_PATH))

from python_client import LLMClient, LLMConfig, MockTransport, StaticTransport


def main() -> None:
    client = LLMClient(
        config=LLMConfig(model="mock-model"),
        transport=MockTransport(),
    )
    response = client.generate_text(
        "Explique le rôle d'un client LLM en une phrase.",
        user_input="Contexte: bootcamp AI Engineering",
    )
    print(response.text)

    json_client = LLMClient(
        config=LLMConfig(model="static-model"),
        transport=StaticTransport(
            '{"label": "technical", "confidence": 0.92, "reason": "Le texte parle de client LLM."}'
        ),
    )
    result = json_client.generate_json(
        "Classe ce texte.",
        required_fields=["label", "confidence", "reason"],
    )
    print(result)


if __name__ == "__main__":
    main()
