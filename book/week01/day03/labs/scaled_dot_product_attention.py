"""Scaled dot-product attention from scratch.

This module is intentionally small and dependency-light for Week 1, Day 3.
It demonstrates the core operation used inside Transformer attention layers.
"""

from __future__ import annotations

import math
from typing import Optional, Tuple

import numpy as np


def stable_softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Compute a numerically stable softmax.

    Args:
        x: Input array.
        axis: Axis over which probabilities are normalized.

    Returns:
        Array with positive values summing to one along `axis`.
    """
    x = np.asarray(x, dtype=float)
    shifted = x - np.max(x, axis=axis, keepdims=True)
    exp = np.exp(shifted)
    denominator = np.sum(exp, axis=axis, keepdims=True)
    return exp / denominator


def causal_mask(query_length: int, key_length: int) -> np.ndarray:
    """Create a boolean causal mask.

    True means attention is allowed. False means the score is masked.
    """
    if query_length <= 0 or key_length <= 0:
        raise ValueError("query_length and key_length must be positive.")
    return np.tril(np.ones((query_length, key_length), dtype=bool))


def scaled_dot_product_attention(
    Q: np.ndarray,
    K: np.ndarray,
    V: np.ndarray,
    mask: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute scaled dot-product attention.

    Args:
        Q: Query matrix of shape (n_queries, d_k).
        K: Key matrix of shape (n_keys, d_k).
        V: Value matrix of shape (n_keys, d_v).
        mask: Optional boolean matrix of shape (n_queries, n_keys).
              True values are kept, False values are blocked.

    Returns:
        A tuple `(output, weights)`.
    """
    Q = np.asarray(Q, dtype=float)
    K = np.asarray(K, dtype=float)
    V = np.asarray(V, dtype=float)

    if Q.ndim != 2 or K.ndim != 2 or V.ndim != 2:
        raise ValueError("Q, K and V must be 2D matrices.")
    if Q.shape[1] != K.shape[1]:
        raise ValueError("Q and K must have the same feature dimension.")
    if K.shape[0] != V.shape[0]:
        raise ValueError("K and V must have the same sequence length.")

    scores = (Q @ K.T) / math.sqrt(K.shape[1])

    if mask is not None:
        mask = np.asarray(mask, dtype=bool)
        if mask.shape != scores.shape:
            raise ValueError("mask must have shape (n_queries, n_keys).")
        scores = np.where(mask, scores, -1e9)

    weights = stable_softmax(scores, axis=-1)
    output = weights @ V
    return output, weights


def demo() -> None:
    """Run a tiny attention example."""
    Q = np.array([[1.0, 0.0], [0.0, 1.0]])
    K = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    V = np.array([[10.0, 0.0], [0.0, 5.0], [3.0, 3.0]])

    output, weights = scaled_dot_product_attention(Q, K, V)

    print("Attention weights:")
    print(np.round(weights, 4))
    print("Row sums:")
    print(np.round(weights.sum(axis=-1), 4))
    print("Contextualized output:")
    print(np.round(output, 4))


if __name__ == "__main__":
    demo()
