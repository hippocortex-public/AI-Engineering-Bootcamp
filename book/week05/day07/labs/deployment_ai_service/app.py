import json
import logging
from time import perf_counter
from typing import Annotated
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Request, Security
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from fastapi.security import APIKeyHeader
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, Counter, Histogram, generate_latest
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .auth import IdentityStore, Principal
from .settings import Settings
from .storage import BackendUnavailable, DocumentNotFound, PermissionDenied, PgRepository, RedisBackend, RateLimited, require_scope

logger = logging.getLogger("deployment_ai_service.audit")
key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    message: str = Field(min_length=1, max_length=2000)
    document_id: str | None = Field(default=None, pattern=r"^[a-z0-9_-]{1,64}$")

    @field_validator("message")
    @classmethod
    def non_blank(cls, message):
        if not message.strip():
            raise ValueError("Blank message")
        return message


def create_app(identities: IdentityStore | None = None, repository=None, backend=None, release="test"):
    if identities is None or repository is None or backend is None:
        settings = Settings.from_environment()
        identities = settings.identities
        repository = PgRepository(settings)
        backend = RedisBackend.from_settings(settings)
        release = settings.release
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    app = FastAPI(title="Deployable AI Service", docs_url=None, redoc_url=None, openapi_url=None)
    registry = CollectorRegistry()
    requests = Counter("ai_http_requests_total", "HTTP requests", ["route", "status"], registry=registry)
    latency = Histogram("ai_http_request_duration_seconds", "HTTP duration", ["route"], registry=registry)
    hits = Counter("ai_cache_hits_total", "Answer cache hits", registry=registry)
    app.state.release = release

    @app.middleware("http")
    async def observe(request: Request, call_next):
        request.state.request_id = f"req_{uuid4().hex}"
        started, status = perf_counter(), 500
        try:
            response = await call_next(request)
            status = response.status_code
            response.headers["X-Request-ID"] = request.state.request_id
            response.headers["Cache-Control"] = "no-store"
            response.headers["X-Content-Type-Options"] = "nosniff"
            return response
        finally:
            route = getattr(request.scope.get("route"), "path", "unmatched")
            if route in {"/chat", "/documents/{document_id}"}:
                requests.labels(route, str(status)).inc()
                latency.labels(route).observe(perf_counter() - started)
            principal = getattr(request.state, "principal", None)
            logger.info(json.dumps({"event": "request_completed", "request_id": request.state.request_id,
                "route": route, "status": status, "subject": principal.subject if principal else None,
                "tenant": principal.tenant if principal else None}))

    def error(request, status, code, headers=None):
        return JSONResponse(status_code=status, content={"error": code, "request_id": request.state.request_id}, headers=headers)

    @app.exception_handler(RequestValidationError)
    async def invalid(request, exc):
        return error(request, 422, "invalid_request")

    @app.exception_handler(BackendUnavailable)
    async def unavailable(request, exc):
        return error(request, 503, "dependency_unavailable", {"Retry-After": "3"})

    @app.exception_handler(DocumentNotFound)
    async def not_found(request, exc):
        return error(request, 404, "not_found")

    @app.exception_handler(PermissionDenied)
    async def forbidden(request, exc):
        return error(request, 403, "forbidden")

    @app.exception_handler(RateLimited)
    async def limited(request, exc):
        return error(request, 429, "rate_limited", {"Retry-After": str(exc.retry_after)})

    @app.exception_handler(Exception)
    async def internal(request, exc):
        return error(request, 500, "internal_error", {"X-Request-ID": request.state.request_id, "Cache-Control": "no-store"})

    def authenticate(request: Request, key: Annotated[str | None, Security(key_header)]):
        principal = identities.authenticate(key)
        if principal is None:
            raise HTTPException(401, "unauthorized", headers={"WWW-Authenticate": "APIKey"})
        request.state.principal = principal
        return principal

    def protected(scope, consume=True):
        def check(principal: Annotated[Principal, Depends(authenticate)]):
            require_scope(principal, scope)
            if consume:
                backend.consume(principal)
            return principal
        return check

    @app.get("/health/live")
    def live():
        return {"status": "alive"}

    @app.get("/health/ready")
    def ready():
        pg_ok = repository.ready()
        redis_ok = backend.ready()
        status = 200 if pg_ok and redis_ok else 503
        return JSONResponse(status_code=status, content={"status": "ready" if status == 200 else "not_ready"})

    @app.get("/metrics")
    def metrics(principal: Annotated[Principal, Depends(protected("metrics:read", consume=False))]):
        return Response(generate_latest(registry), headers={"Content-Type": CONTENT_TYPE_LATEST})

    @app.get("/documents/{document_id}")
    def document(document_id: str, principal: Annotated[Principal, Depends(protected("documents:read"))]):
        result = repository.get(principal, document_id)
        return {"document_id": result.document_id, "content": result.content}

    @app.post("/chat")
    def chat(payload: ChatRequest, principal: Annotated[Principal, Depends(protected("chat:write"))]):
        # Autorisation et récupération avant le cache, même lors d'un cache hit.
        document = repository.get(principal, payload.document_id) if payload.document_id else None
        key = backend.cache_key(principal, payload.message, document)
        answer = backend.get_answer(key)
        cached = answer is not None
        if cached:
            hits.inc()
        else:
            answer = f"Document autorisé : {document.document_id}. {document.content[:200]}" if document else "Réponse IA simulée et déployable."
            backend.put_answer(key, answer)
        return {"answer": answer, "cached": cached, "provider": "simulated"}

    return app
