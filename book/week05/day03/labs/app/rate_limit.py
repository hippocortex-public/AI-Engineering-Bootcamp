async def allow_request(redis, key: str, limit: int, ttl_seconds: int) -> bool:
    """Fixed-window rate limiter using Redis INCR and EXPIRE."""
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, ttl_seconds)
    return count <= limit
