from concurrent.futures import ThreadPoolExecutor

import pytest
import redis

from deployment_ai_service.auth import Principal
from deployment_ai_service.storage import BackendUnavailable, Document, RateLimited, RedisBackend


def principal(tenant="alpha", subject="alice"):
    return Principal(subject, tenant, frozenset({"chat:write"}))


def test_lua_limits_requests_and_sets_expiry(redis_client):
    backend = RedisBackend(redis_client, limit=2, window=60)
    backend.consume(principal())
    backend.consume(principal())
    with pytest.raises(RateLimited) as exc:
        backend.consume(principal())
    assert 1 <= exc.value.retry_after <= 60
    assert 0 < redis_client.ttl("quota:alpha:alice") <= 60
    assert int(redis_client.get("quota:alpha:alice")) == 2


def test_lua_is_shared_between_api_instances(redis_client):
    one, two = RedisBackend(redis_client, limit=1), RedisBackend(redis_client, limit=1)
    one.consume(principal())
    with pytest.raises(RateLimited):
        two.consume(principal())
    two.consume(principal("beta"))


def test_concurrent_requests_never_exceed_allowance(redis_client):
    backend = RedisBackend(redis_client, limit=7)
    def attempt(_):
        try:
            backend.consume(principal())
            return 1
        except RateLimited:
            return 0
    with ThreadPoolExecutor(max_workers=8) as pool:
        assert sum(pool.map(attempt, range(40))) == 7


def test_expired_window_can_be_created_again(redis_client):
    backend = RedisBackend(redis_client, limit=1)
    backend.consume(principal())
    redis_client.delete("quota:alpha:alice")
    backend.consume(principal())
    assert redis_client.ttl("quota:alpha:alice") > 0


def test_cache_is_partitioned_by_tenant_subject_and_document():
    document = Document("guide", "secret")
    key = RedisBackend.cache_key(principal(), "Question", document)
    assert key != RedisBackend.cache_key(principal("beta"), "Question", document)
    assert key != RedisBackend.cache_key(principal(subject="carol"), "Question", document)
    assert key != RedisBackend.cache_key(principal(), "Question", Document("guide", "changed"))
    assert "secret" not in key and "Question" not in key


def test_cache_ttl_is_bounded(redis_client):
    backend = RedisBackend(redis_client)
    backend.put_answer("answer:test", "Hello")
    assert backend.get_answer("answer:test") == "Hello"
    assert 0 < redis_client.ttl("answer:test") <= 120


def test_readiness_catches_redis_errors(redis_client, monkeypatch):
    def fail():
        raise redis.ConnectionError("private")
    monkeypatch.setattr(redis_client, "ping", fail)
    assert RedisBackend(redis_client).ready() is False
