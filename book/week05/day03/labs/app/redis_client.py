import os
from collections.abc import AsyncIterator

import redis.asyncio as redis


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


async def get_redis() -> AsyncIterator[redis.Redis]:
    client = redis.from_url(REDIS_URL, decode_responses=True)
    try:
        yield client
    finally:
        await client.aclose()
