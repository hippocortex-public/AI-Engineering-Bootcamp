import json
import os
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException
from redis.asyncio import Redis

from app.cache import build_llm_cache_key, get_cached_json, set_cached_json
from app.rate_limit import allow_request
from app.redis_client import get_redis
from app.schemas import ChatRequest, ChatResponse


APP_NAME = os.getenv("APP_NAME", "ai-api")
APP_ENV = os.getenv("APP_ENV", "dev")

CACHE_TTL_SECONDS = 3600
SESSION_TTL_SECONDS = 3600
RATE_LIMIT_TTL_SECONDS = 60
RATE_LIMIT_PER_MINUTE = 20

app = FastAPI(title="AI Engineering Bootcamp - Redis Day")


def fake_llm_call(message: str) -> dict[str, str]:
    """Deterministic LLM simulation for a reproducible lab."""
    return {
        "answer": (
            "Réponse simulée: Redis aide une API IA avec le cache, "
            f"l'état court et le rate limiting. Message reçu: {message}"
        )
    }


def session_key(user_id: str, conversation_id: str) -> str:
    return f"{APP_NAME}:{APP_ENV}:session:user:{user_id}:conv:{conversation_id}"


def rate_limit_key(user_id: str) -> str:
    return f"{APP_NAME}:{APP_ENV}:ratelimit:user:{user_id}:minute"


async def append_session_message(redis: Redis, key: str, role: str, content: str) -> None:
    raw = await redis.get(key)
    if raw:
        session = json.loads(raw)
    else:
        session = {"messages": []}

    session["messages"].append({
        "role": role,
        "content": content,
        "at": datetime.now(timezone.utc).isoformat(),
    })
    session["messages"] = session["messages"][-10:]
    await redis.set(key, json.dumps(session, ensure_ascii=False), ex=SESSION_TTL_SECONDS)


@app.get("/health")
async def health(redis: Redis = Depends(get_redis)) -> dict[str, str]:
    try:
        await redis.ping()
        redis_status = "ok"
    except Exception:
        redis_status = "unavailable"
    return {"status": "ok", "redis": redis_status}


@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, redis: Redis = Depends(get_redis)) -> ChatResponse:
    try:
        allowed = await allow_request(
            redis,
            rate_limit_key(payload.user_id),
            limit=RATE_LIMIT_PER_MINUTE,
            ttl_seconds=RATE_LIMIT_TTL_SECONDS,
        )
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Rate limiter unavailable") from exc

    if not allowed:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    cache_payload = {
        "user_id": payload.user_id,
        "conversation_id": payload.conversation_id,
        "message": payload.message,
    }
    cache_key = build_llm_cache_key(
        APP_NAME,
        APP_ENV,
        payload.model,
        payload.prompt_version,
        cache_payload,
    )

    try:
        cached = await get_cached_json(redis, cache_key)
    except Exception:
        cached = None

    if cached is not None:
        return ChatResponse(source="cache", answer=cached["answer"], cache_key=cache_key)

    result = fake_llm_call(payload.message)

    try:
        await set_cached_json(redis, cache_key, result, ttl_seconds=CACHE_TTL_SECONDS)
        skey = session_key(payload.user_id, payload.conversation_id)
        await append_session_message(redis, skey, "user", payload.message)
        await append_session_message(redis, skey, "assistant", result["answer"])
    except Exception:
        # Cache and session failures degrade gracefully after the model result exists.
        pass

    return ChatResponse(source="llm", answer=result["answer"], cache_key=cache_key)


@app.get("/sessions/{user_id}/{conversation_id}")
async def get_session(user_id: str, conversation_id: str, redis: Redis = Depends(get_redis)):
    raw = await redis.get(session_key(user_id, conversation_id))
    if raw is None:
        return {"messages": []}
    return json.loads(raw)
