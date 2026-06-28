import numpy as np
import pytest

from book.week01.day03.labs.scaled_dot_product_attention import (
    causal_mask,
    scaled_dot_product_attention,
    stable_softmax,
)
from book.week01.day03.labs.tiny_transformer_block import TinyTransformerBlock


def test_softmax_rows_sum_to_one():
    x = np.array([[2.0, 1.0, 0.0], [1.0, 1.0, 1.0]])
    probs = stable_softmax(x, axis=-1)
    assert np.allclose(probs.sum(axis=-1), np.ones(2))


def test_attention_prefers_aligned_key():
    Q = np.array([[1.0, 0.0]])
    K = np.array([[1.0, 0.0], [0.0, 1.0]])
    V = np.array([[10.0, 0.0], [0.0, 5.0]])

    output, weights = scaled_dot_product_attention(Q, K, V)

    assert weights.shape == (1, 2)
    assert output.shape == (1, 2)
    assert weights[0, 0] > weights[0, 1]


def test_causal_mask_blocks_future_positions():
    Q = np.eye(3)
    K = np.eye(3)
    V = np.arange(9, dtype=float).reshape(3, 3)
    mask = causal_mask(3, 3)

    _, weights = scaled_dot_product_attention(Q, K, V, mask=mask)

    assert np.allclose(weights[0, 1:], [0.0, 0.0])
    assert weights[1, 2] == pytest.approx(0.0)


def test_invalid_shapes_raise_value_error():
    Q = np.ones((2, 3))
    K = np.ones((2, 4))
    V = np.ones((2, 3))

    with pytest.raises(ValueError):
        scaled_dot_product_attention(Q, K, V)


def test_tiny_transformer_block_preserves_shape():
    x = np.ones((5, 4))
    block = TinyTransformerBlock.with_seed(model_dim=4, hidden_dim=8)
    y = block.forward(x)
    assert y.shape == x.shape
