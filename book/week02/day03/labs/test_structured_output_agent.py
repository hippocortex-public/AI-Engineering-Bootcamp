"""
Tests du lab Structured Outputs.

Exécution :
    python test_structured_output_agent.py
"""

from structured_output_agent import (
    StructuredOutputError,
    parse_triage_output,
    triage_ticket,
)


VALID_OUTPUT = """
{
  "category": "billing",
  "priority": "high",
  "sentiment": "angry",
  "summary": "Le client signale une double facturation.",
  "action_required": true,
  "next_action": {
    "owner_team": "billing_ops",
    "rationale": "Le ticket mentionne un paiement prélevé deux fois."
  },
  "confidence": 0.91
}
"""


def assert_raises(expected_exception, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except expected_exception:
        return
    except Exception as exc:
        raise AssertionError(
            f"Expected {expected_exception.__name__}, got {type(exc).__name__}: {exc}"
        ) from exc

    raise AssertionError(f"Expected {expected_exception.__name__} to be raised")


def test_valid_output_is_mapped_to_domain_object():
    decision = parse_triage_output(VALID_OUTPUT)

    assert decision.category == "billing"
    assert decision.priority == "high"
    assert decision.sentiment == "angry"
    assert decision.owner_team == "billing_ops"
    assert decision.confidence == 0.91
    assert decision.action_required is True


def test_invalid_enum_is_rejected():
    invalid_output = """
    {
      "category": "finance",
      "priority": "high",
      "sentiment": "angry",
      "summary": "Le client signale une double facturation.",
      "action_required": true,
      "next_action": {
        "owner_team": "billing_ops",
        "rationale": "Le ticket mentionne un paiement prélevé deux fois."
      },
      "confidence": 0.91
    }
    """

    assert_raises(StructuredOutputError, parse_triage_output, invalid_output)


def test_missing_required_field_is_rejected():
    invalid_output = """
    {
      "category": "billing",
      "priority": "high",
      "sentiment": "angry",
      "summary": "Le client signale une double facturation.",
      "action_required": true,
      "next_action": {
        "owner_team": "billing_ops",
        "rationale": "Le ticket mentionne un paiement prélevé deux fois."
      }
    }
    """

    assert_raises(StructuredOutputError, parse_triage_output, invalid_output)


def test_extra_field_is_rejected():
    invalid_output = """
    {
      "category": "billing",
      "priority": "high",
      "sentiment": "angry",
      "summary": "Le client signale une double facturation.",
      "action_required": true,
      "next_action": {
        "owner_team": "billing_ops",
        "rationale": "Le ticket mentionne un paiement prélevé deux fois."
      },
      "confidence": 0.91,
      "refund_amount": 100
    }
    """

    assert_raises(StructuredOutputError, parse_triage_output, invalid_output)


def test_confidence_out_of_range_is_rejected():
    invalid_output = """
    {
      "category": "billing",
      "priority": "high",
      "sentiment": "angry",
      "summary": "Le client signale une double facturation.",
      "action_required": true,
      "next_action": {
        "owner_team": "billing_ops",
        "rationale": "Le ticket mentionne un paiement prélevé deux fois."
      },
      "confidence": 1.2
    }
    """

    assert_raises(StructuredOutputError, parse_triage_output, invalid_output)


def test_agent_routes_billing_ticket():
    decision = triage_ticket("Je suis très énervé, vous m’avez facturé deux fois.")

    assert decision.category == "billing"
    assert decision.priority == "high"
    assert decision.owner_team == "billing_ops"
    assert decision.action_required is True


def run_all_tests():
    tests = [
        test_valid_output_is_mapped_to_domain_object,
        test_invalid_enum_is_rejected,
        test_missing_required_field_is_rejected,
        test_extra_field_is_rejected,
        test_confidence_out_of_range_is_rejected,
        test_agent_routes_billing_ticket,
    ]

    for test in tests:
        test()

    print(f"{len(tests)} tests passed")


if __name__ == "__main__":
    run_all_tests()
