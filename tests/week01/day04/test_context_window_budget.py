from book.week01.day04.labs.context_window_budget import build_context_plan, estimate_tokens


def test_estimate_tokens_ceil():
    assert estimate_tokens("abcde", chars_per_token=4) == 2


def test_context_plan_fits():
    plan = build_context_plan(
        context_window=100,
        reserved_output_tokens=20,
        sections={"system": "abcd", "question": "abcdefgh"},
        chars_per_token=4,
    )
    assert plan["fits"] is True
    assert plan["estimated_input_tokens"] == 3
    assert plan["remaining_tokens"] == 77


def test_context_plan_overflow_recommends_actions():
    plan = build_context_plan(
        context_window=10,
        reserved_output_tokens=3,
        sections={"documents": "x" * 100},
        chars_per_token=4,
    )
    assert plan["fits"] is False
    assert len(plan["recommendations"]) >= 3
