# Corrigé — Challenge Jour 4

## Solution de référence

```python
from math import ceil
from pprint import pprint

def estimate_tokens(text: str, chars_per_token: float = 4.0) -> int:
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
            "Reserve a stricter maximum output size.",
            "Rank chunks by relevance and keep only the highest-value passages.",
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

if __name__ == "__main__":
    sections = {
        "system": "You are a precise AI engineering assistant.",
        "history": "Previous conversation. " * 500,
        "documents": "Technical documentation. " * 1200,
        "question": "Explain how token budgeting should work.",
    }

    pprint(build_context_plan(
        context_window=16000,
        reserved_output_tokens=1500,
        sections=sections,
    ))
```

## Commentaire

Cette solution reste volontairement approximative. En production, il faut utiliser le tokenizer réel du modèle cible. L’intérêt pédagogique est de rendre visible le budget avant l’appel LLM.
