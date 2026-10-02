from monitoring_ai_service.alerts import evaluate_alerts


def test_evaluate_alerts_detects_all_thresholds() -> None:
    snapshot = {
        "error_rate": 0.07,
        "p95_latency_ms": 4200,
        "estimated_cost_usd": 83.5,
        "empty_response_count": 18,
    }

    alerts = evaluate_alerts(snapshot)
    names = {alert.name for alert in alerts}

    assert names == {
        "high_error_rate",
        "high_p95_latency",
        "high_estimated_cost",
        "empty_response_spike",
    }


def test_evaluate_alerts_returns_empty_list_when_healthy() -> None:
    snapshot = {
        "error_rate": 0.0,
        "p95_latency_ms": 800,
        "estimated_cost_usd": 10.0,
        "empty_response_count": 0,
    }

    assert evaluate_alerts(snapshot) == []
