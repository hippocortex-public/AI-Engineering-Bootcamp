from __future__ import annotations

import json
import logging
from time import perf_counter

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .alerts import evaluate_alerts
from .cost import estimate_cost_usd
from .metrics import MetricsStore, RequestRecord
from .redaction import redact_sensitive_text
from .schemas import ChatRequest, ChatResponse, HealthResponse

app = FastAPI(title="Monitoring AI Service Lab", version="1.0.0")
metrics_store = MetricsStore()
logger = logging.getLogger("uvicorn.error")


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request.state.request_id = metrics_store.new_request_id()
    started = perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    logger.info(json.dumps({
        "event": "http_request_completed",
        "request_id": request.state.request_id,
        "method": request.method,
        "status_code": response.status_code,
        "latency_ms": round((perf_counter() - started) * 1000, 3),
    }))
    return response


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="monitoring-ai-service",
        checks={
            "api": "ok",
            "metrics_store": "ok",
            "model_provider": "simulated",
        },
    )


@app.get("/metrics")
def metrics() -> dict:
    return metrics_store.snapshot()


@app.get("/alerts")
def alerts() -> list[dict]:
    snapshot = metrics_store.snapshot()
    return [alert.__dict__ for alert in evaluate_alerts(snapshot)]


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, request: Request) -> ChatResponse:
    started = perf_counter()
    request_id = request.state.request_id

    try:
        safe_message = redact_sensitive_text(payload.message)
        answer = simulate_model_answer(safe_message)

        prompt_tokens = estimate_tokens(payload.message)
        completion_tokens = estimate_tokens(answer)
        estimated_cost = estimate_cost_usd(prompt_tokens, completion_tokens)

        latency_ms = (perf_counter() - started) * 1000
        metrics_store.record(
            RequestRecord(
                request_id=request_id,
                route="/chat",
                status_code=200,
                latency_ms=latency_ms,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                estimated_cost_usd=estimated_cost,
                empty_response=(answer.strip() == ""),
            )
        )

        return ChatResponse(
            request_id=request_id,
            answer=answer,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            estimated_cost_usd=estimated_cost,
        )
    except Exception:
        latency_ms = (perf_counter() - started) * 1000
        metrics_store.record(
            RequestRecord(
                request_id=request_id,
                route="/chat",
                status_code=500,
                latency_ms=latency_ms,
                prompt_tokens=0,
                completion_tokens=0,
                estimated_cost_usd=0.0,
                empty_response=True,
            )
        )
        return JSONResponse(
            status_code=500,
            content={
                "request_id": request_id,
                "error": "internal_error",
                "detail": "Une erreur interne est survenue.",
            },
        )


def simulate_model_answer(message: str) -> str:
    """Simule une réponse LLM déterministe pour le lab."""

    normalized = message.strip().lower()
    if "empty" in normalized or "réponse vide" in normalized:
        return ""

    return (
        "Un système IA en production doit être monitoré sur la latence, "
        "les erreurs, les tokens, le coût estimé et la qualité observable."
    )


def estimate_tokens(text: str) -> int:
    """Approximation pédagogique : environ un token pour quatre caractères."""

    return max(1, len(text) // 4)
