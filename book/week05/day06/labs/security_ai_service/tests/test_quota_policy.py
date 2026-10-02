from concurrent.futures import ThreadPoolExecutor

import pytest

from security_ai_service.auth import Principal
from security_ai_service.policy import AccessDenied, Document, DocumentStore, ToolPolicy
from security_ai_service.quota import FixedWindowLimiter, QuotaExceeded
from conftest import ALL_SCOPES


def test_concurrent_quota_never_over_admits():
    limiter = FixedWindowLimiter(7, clock=lambda: 0.0)
    principal = Principal("alice", "alpha", ALL_SCOPES)
    def attempt(_):
        try:
            limiter.consume(principal)
            return 1
        except QuotaExceeded:
            return 0
    with ThreadPoolExecutor(max_workers=8) as pool:
        assert sum(pool.map(attempt, range(50))) == 7


def test_equal_subject_names_in_distinct_tenants_do_not_share_quota():
    limiter = FixedWindowLimiter(1)
    limiter.consume(Principal("alice", "alpha", ALL_SCOPES))
    limiter.consume(Principal("alice", "beta", ALL_SCOPES))


def test_retry_after_rounds_up():
    clock = [0.0]
    limiter = FixedWindowLimiter(1, 60, lambda: clock[0])
    principal = Principal("alice", "alpha", ALL_SCOPES)
    limiter.consume(principal)
    clock[0] = 59.2
    with pytest.raises(QuotaExceeded) as exc:
        limiter.consume(principal)
    assert exc.value.retry_after == 1


def test_document_scope_is_required_even_when_tool_scope_exists():
    principal = Principal("alice", "alpha", frozenset({"tools:read"}))
    ToolPolicy().authorize(principal, "read_document")
    with pytest.raises(AccessDenied):
        DocumentStore([Document("alpha-guide", "alpha", "secret")]).get(principal, "alpha-guide")


@pytest.mark.parametrize("limit,seconds", [(0, 60), (10, 0), (10, float("inf"))])
def test_invalid_quota_configuration(limit, seconds):
    with pytest.raises(ValueError):
        FixedWindowLimiter(limit, seconds)
