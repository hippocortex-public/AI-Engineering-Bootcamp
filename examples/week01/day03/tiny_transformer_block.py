"""A tiny Transformer-like block for educational purposes.

This is not a production implementation. It is designed to make the shape
and data flow of a Transformer block explicit for Week 1, Day 3.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

try:
    from .scaled_dot_product_attention import scaled_dot_product_attention
except ImportError:  # Allows direct execution from the file path.
    from scaled_dot_product_attention import scaled_dot_product_attention


def layer_norm(x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """Apply simple layer normalization on the last dimension."""
    x = np.asarray(x, dtype=float)
    mean = x.mean(axis=-1, keepdims=True)
    variance = x.var(axis=-1, keepdims=True)
    return (x - mean) / np.sqrt(variance + eps)


@dataclass
class TinyTransformerBlock:
    """Minimal single-head Transformer-like block."""

    W_q: np.ndarray
    W_k: np.ndarray
    W_v: np.ndarray
    W_ff1: np.ndarray
    W_ff2: np.ndarray

    @classmethod
    def with_seed(cls, model_dim: int, hidden_dim: int, seed: int = 7) -> "TinyTransformerBlock":
        rng = np.random.default_rng(seed)
        scale = 0.1
        return cls(
            W_q=rng.normal(0, scale, size=(model_dim, model_dim)),
            W_k=rng.normal(0, scale, size=(model_dim, model_dim)),
            W_v=rng.normal(0, scale, size=(model_dim, model_dim)),
            W_ff1=rng.normal(0, scale, size=(model_dim, hidden_dim)),
            W_ff2=rng.normal(0, scale, size=(hidden_dim, model_dim)),
        )

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Run a forward pass.

        Args:
            x: Matrix of shape (sequence_length, model_dim).

        Returns:
            Matrix of shape (sequence_length, model_dim).
        """
        x = np.asarray(x, dtype=float)
        q = x @ self.W_q
        k = x @ self.W_k
        v = x @ self.W_v

        attention_output, _ = scaled_dot_product_attention(q, k, v)
        x = layer_norm(x + attention_output)

        ff = np.maximum(0.0, x @ self.W_ff1) @ self.W_ff2
        return layer_norm(x + ff)


def demo() -> None:
    x = np.array(
        [
            [1.0, 0.0, 0.5, 0.2],
            [0.3, 0.8, 0.1, 0.0],
            [0.0, 0.2, 0.9, 0.7],
        ]
    )
    block = TinyTransformerBlock.with_seed(model_dim=4, hidden_dim=8)
    y = block.forward(x)
    print("Input shape:", x.shape)
    print("Output shape:", y.shape)
    print(np.round(y, 4))


if __name__ == "__main__":
    demo()
