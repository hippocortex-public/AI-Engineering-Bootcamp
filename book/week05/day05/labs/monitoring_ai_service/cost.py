from dataclasses import dataclass


@dataclass(frozen=True)
class ModelPricing:
    """Prix fictif par 1000 tokens.

    Les valeurs du lab ne représentent pas un fournisseur réel. Elles servent
    uniquement à rendre l'estimation déterministe et testable.
    """

    input_per_1k_usd: float
    output_per_1k_usd: float


DEFAULT_PRICING = ModelPricing(input_per_1k_usd=0.002, output_per_1k_usd=0.006)


def estimate_cost_usd(
    prompt_tokens: int,
    completion_tokens: int,
    pricing: ModelPricing = DEFAULT_PRICING,
) -> float:
    """Estime le coût d'une requête IA à partir de la consommation de tokens."""

    if prompt_tokens < 0 or completion_tokens < 0:
        raise ValueError("Token counts must be positive or zero.")

    cost = (
        prompt_tokens / 1000 * pricing.input_per_1k_usd
        + completion_tokens / 1000 * pricing.output_per_1k_usd
    )
    return round(cost, 6)
