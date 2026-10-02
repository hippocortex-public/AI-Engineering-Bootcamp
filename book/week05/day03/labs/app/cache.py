import hashlib
import json
from typing import Any


def canonical_json(payload: dict[str, Any]) -> str:
    """Serialize a payload in a stable way for hashing."""
    return json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def build_llm_cache_key(
    app: str,
    env: str,
    model: str,
    prompt_version: str,
    payload: dict[str, Any],
) -> str:
    """Build a Redis key without leaking prompt content into the key name."""
    digest = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()[:16]
    return f"{app}:{env}:cache:llm:{model}:{prompt_version}:hash:{digest}"


async def get_cached_json(redis, key: str) -> dict[str, Any] | None:
    raw = await redis.get(key)
    if raw is None:
        return None
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    return json.loads(raw)


async def set_cached_json(redis, key: str, value: dict[str, Any], ttl_seconds: int) -> None:
    await redis.set(key, json.dumps(value, ensure_ascii=False), ex=ttl_seconds)
