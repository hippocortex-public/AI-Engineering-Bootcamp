from monitoring_ai_service.cost import estimate_cost_usd


def test_estimate_cost_usd() -> None:
    cost = estimate_cost_usd(prompt_tokens=1500, completion_tokens=400)
    assert cost == 0.0054


def test_estimate_cost_rejects_negative_tokens() -> None:
    try:
        estimate_cost_usd(prompt_tokens=-1, completion_tokens=10)
    except ValueError as exc:
        assert "Token counts" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
