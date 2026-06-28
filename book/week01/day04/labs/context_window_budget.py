from math import ceil
from pprint import pprint


def estimate_tokens(text: str, chars_per_token: float = 4.0) -> int:
    """Estimate tokens using a rough character/token ratio."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if chars_per_token <= 0:
        raise ValueError("chars_per_token must be positive")
    return ceil(len(text) / chars_per_token)


def build_context_plan(
    context_window: int,
    reserved_output_tokens: int,
    sections: dict[str, str],
    chars_per_token: float = 4.0,
) -> dict:
    """Build a context budget plan before an LLM call."""
    if context_window <= 0:
        raise ValueError("context_window must be positive")
    if reserved_output_tokens < 0:
        raise ValueError("reserved_output_tokens cannot be negative")
    if reserved_output_tokens >= context_window:
        raise ValueError("reserved_output_tokens must be smaller than context_window")
    if not isinstance(sections, dict):
        raise TypeError("sections must be a dictionary")

    section_tokens = {
        name: estimate_tokens(value, chars_per_token)
        for name, value in sections.items()
    }

    estimated_input_tokens = sum(section_tokens.values())
    remaining_tokens = context_window - reserved_output_tokens - estimated_input_tokens
    fits = remaining_tokens >= 0

    recommendations = []
    if not fits:
        recommendations = [
            "Reduce retrieved documents before calling the model.",
            "Summarize old conversation history.",
            "Apply chunk ranking and keep only the highest-value passages.",
            "Lower the maximum output size when business requirements allow it.",
        ]

    return {
        "context_window": context_window,
        "reserved_output_tokens": reserved_output_tokens,
        "estimated_input_tokens": estimated_input_tokens,
        "remaining_tokens": remaining_tokens,
        "fits": fits,
        "sections": section_tokens,
        "recommendations": recommendations,
    }


def main() -> None:
    sections = {
        "system": "You are an AI Engineering assistant focused on correctness.",
        "history": "User and assistant discussed transformers. " * 300,
        "documents": "Documentation about tokens, BPE and context windows. " * 900,
        "question": "How should we reduce context before calling the model?",
    }

    plan = build_context_plan(
        context_window=16000,
        reserved_output_tokens=1500,
        sections=sections,
    )
    pprint(plan)


if __name__ == "__main__":
    main()
