from monitoring_ai_service.metrics import MetricsStore, RequestRecord, percentile


def make_record(
    latency_ms: float,
    status_code: int = 200,
    prompt_tokens: int = 100,
    completion_tokens: int = 50,
    cost: float = 0.001,
    empty_response: bool = False,
) -> RequestRecord:
    return RequestRecord(
        request_id="req_test",
        route="/chat",
        status_code=status_code,
        latency_ms=latency_ms,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        estimated_cost_usd=cost,
        empty_response=empty_response,
    )


def test_metrics_snapshot_aggregates_requests() -> None:
    store = MetricsStore()
    store.record(make_record(latency_ms=100))
    store.record(make_record(latency_ms=200, status_code=500, empty_response=True))

    snapshot = store.snapshot()

    assert snapshot["request_count"] == 2
    assert snapshot["error_count"] == 1
    assert snapshot["error_rate"] == 0.5
    assert snapshot["empty_response_count"] == 1
    assert snapshot["total_prompt_tokens"] == 200
    assert snapshot["total_completion_tokens"] == 100
    assert snapshot["estimated_cost_usd"] == 0.002


def test_percentile_returns_expected_value() -> None:
    assert percentile([100, 200, 300, 400, 500], 95) == 500


def test_metrics_reject_negative_latency() -> None:
    store = MetricsStore()
    try:
        store.record(make_record(latency_ms=-1))
    except ValueError as exc:
        assert "latency_ms" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
