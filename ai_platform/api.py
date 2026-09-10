"""
FastAPI API layer for the AI Engineering Bootcamp.

Week 5 Day 2 turns the production architecture into a testable HTTP API.
The module intentionally keeps the model/service deterministic so that the
training lab can run locally without external credentials.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional
from uuid import uuid4
import re
import time

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator


Intent = Literal["billing", "technical", "account", "general"]
SafetyStatus = Literal["allowed", "needs_review"]


class APISettings(BaseModel):
    """Runtime settings for the HTTP API."""

    model_config = ConfigDict(extra="forbid")

    title: str = "AI Platform API"
    version: str = "0.1.0"
    require_api_key: bool = True
    api_key: str = "dev-secret"
    max_message_chars: int = Field(default=1200, ge=1)
    rate_limit_per_session: int = Field(default=5, ge=1)
    service_name: str = "support-assistant"

    @field_validator("title", "version", "api_key", "service_name")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value must not be blank")
        return value


class ChatRequest(BaseModel):
    """Input contract for a single assistant turn."""

    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(min_length=3, max_length=80)
    user_id: str = Field(min_length=3, max_length=80)
    message: str = Field(min_length=1, max_length=4000)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("session_id", "user_id")
    @classmethod
    def identifier_must_be_safe(cls, value: str) -> str:
        if not re.fullmatch(r"[a-zA-Z0-9_.:-]+", value):
            raise ValueError("identifier must contain only letters, digits, _, ., :, or -")
        return value

    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("message must not be blank")
        return value


class ChatResponse(BaseModel):
    """Output contract returned by the API."""

    model_config = ConfigDict(extra="forbid")

    request_id: str
    session_id: str
    user_id: str
    intent: Intent
    answer: str
    safety_status: SafetyStatus
    trace: List[str] = Field(default_factory=list)


class SessionTranscript(BaseModel):
    """Stored transcript for a session."""

    model_config = ConfigDict(extra="forbid")

    session_id: str
    turns: List[Dict[str, Any]]


class ErrorResponse(BaseModel):
    """Stable error envelope for API clients."""

    model_config = ConfigDict(extra="forbid")

    error: str
    message: str
    request_id: str


@dataclass
class RateLimitDecision:
    """Decision returned by the in-memory rate limiter."""

    allowed: bool
    remaining: int
    limit: int


class InMemoryRateLimiter:
    """Small deterministic rate limiter scoped by session ID.

    This is a lab implementation, not a distributed production limiter.
    """

    def __init__(self, limit: int) -> None:
        if limit < 1:
            raise ValueError("limit must be >= 1")
        self.limit = limit
        self._counts: Dict[str, int] = {}

    def check(self, key: str) -> RateLimitDecision:
        count = self._counts.get(key, 0)
        if count >= self.limit:
            return RateLimitDecision(False, 0, self.limit)
        count += 1
        self._counts[key] = count
        return RateLimitDecision(True, self.limit - count, self.limit)

    def reset(self) -> None:
        self._counts.clear()


class DeterministicSupportService:
    """Deterministic business service standing in for an LLM-backed agent."""

    def __init__(self) -> None:
        self.sessions: Dict[str, List[Dict[str, Any]]] = {}

    def is_ready(self) -> bool:
        return True

    def answer(self, payload: ChatRequest, request_id: str) -> ChatResponse:
        intent = self._classify_intent(payload.message)
        safe_message = self._redact_pii(payload.message)
        safety_status: SafetyStatus = "needs_review" if self._contains_sensitive_action(payload.message) else "allowed"
        answer = self._answer_for(intent=intent, safety_status=safety_status)

        turn = {
            "request_id": request_id,
            "user_id": payload.user_id,
            "message": safe_message,
            "intent": intent,
            "safety_status": safety_status,
            "timestamp": time.time(),
        }
        self.sessions.setdefault(payload.session_id, []).append(turn)

        return ChatResponse(
            request_id=request_id,
            session_id=payload.session_id,
            user_id=payload.user_id,
            intent=intent,
            answer=answer,
            safety_status=safety_status,
            trace=["validated_request", f"classified:{intent}", f"safety:{safety_status}", "stored_turn"],
        )

    def transcript(self, session_id: str) -> SessionTranscript:
        turns = self.sessions.get(session_id)
        if turns is None:
            raise KeyError(session_id)
        return SessionTranscript(session_id=session_id, turns=list(turns))

    @staticmethod
    def _classify_intent(message: str) -> Intent:
        normalized = message.lower()
        if any(word in normalized for word in ("invoice", "billing", "refund", "payment", "facture", "paiement")):
            return "billing"
        if any(word in normalized for word in ("bug", "error", "stacktrace", "latency", "timeout", "erreur")):
            return "technical"
        if any(word in normalized for word in ("login", "password", "account", "compte", "mot de passe")):
            return "account"
        return "general"

    @staticmethod
    def _contains_sensitive_action(message: str) -> bool:
        normalized = message.lower()
        return any(word in normalized for word in ("delete account", "close account", "supprimer mon compte", "refund now"))

    @staticmethod
    def _redact_pii(message: str) -> str:
        message = re.sub(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", "[redacted_email]", message)
        message = re.sub(r"\b(?:\d[ -]*?){13,16}\b", "[redacted_card]", message)
        return message

    @staticmethod
    def _answer_for(intent: Intent, safety_status: SafetyStatus) -> str:
        if safety_status == "needs_review":
            return "Action sensible détectée : validation humaine requise avant exécution."
        answers: Dict[Intent, str] = {
            "billing": "Je peux aider à qualifier la demande de facturation et préparer les informations nécessaires.",
            "technical": "Je peux aider à isoler le problème technique, collecter les symptômes et proposer une prochaine étape.",
            "account": "Je peux aider sur les questions de compte sans exposer de secret ni modifier l'identité utilisateur.",
            "general": "Je peux aider à orienter la demande et demander une précision si nécessaire.",
        }
        return answers[intent]


def build_router(
    *,
    settings: APISettings,
    service: DeterministicSupportService,
    limiter: InMemoryRateLimiter,
) -> APIRouter:
    """Build the authenticated v1 router."""

    def require_api_key(x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")) -> None:
        if settings.require_api_key and x_api_key != settings.api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid or missing API key",
            )

    router = APIRouter(prefix="/v1", tags=["ai"], dependencies=[Depends(require_api_key)])

    @router.post("/chat", response_model=ChatResponse)
    def chat(payload: ChatRequest, request: Request) -> ChatResponse:
        if len(payload.message) > settings.max_message_chars:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="message exceeds configured maximum length",
            )

        decision = limiter.check(payload.session_id)
        if not decision.allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"rate limit exceeded for session {payload.session_id}",
                headers={"X-RateLimit-Limit": str(decision.limit), "X-RateLimit-Remaining": "0"},
            )

        return service.answer(payload, request.state.request_id)

    @router.get("/sessions/{session_id}", response_model=SessionTranscript)
    def get_session(session_id: str) -> SessionTranscript:
        try:
            return service.transcript(session_id)
        except KeyError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="session not found")

    return router


def create_app(
    settings: Optional[APISettings] = None,
    service: Optional[DeterministicSupportService] = None,
    limiter: Optional[InMemoryRateLimiter] = None,
) -> FastAPI:
    """Create the FastAPI application with middleware, health checks and routes."""

    settings = settings or APISettings()
    service = service or DeterministicSupportService()
    limiter = limiter or InMemoryRateLimiter(settings.rate_limit_per_session)

    app = FastAPI(
        title=settings.title,
        version=settings.version,
        summary="Production-facing API for an AI support assistant",
    )

    app.state.settings = settings
    app.state.service = service
    app.state.rate_limiter = limiter

    @app.middleware("http")
    async def request_id_middleware(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or request.headers.get("X-Client-Request-ID") or str(uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        request_id = getattr(request.state, "request_id", "unknown")
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error=str(exc.status_code),
                message=str(exc.detail),
                request_id=request_id,
            ).model_dump(),
            headers=getattr(exc, "headers", None),
        )

    @app.get("/healthz", tags=["system"])
    def healthz() -> Dict[str, str]:
        return {"status": "ok", "service": settings.service_name, "version": settings.version}

    @app.get("/readyz", tags=["system"])
    def readyz() -> Dict[str, str]:
        if not service.is_ready():
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="service not ready")
        return {"status": "ready", "service": settings.service_name}

    app.include_router(build_router(settings=settings, service=service, limiter=limiter))
    return app


app = create_app(APISettings(require_api_key=False))


if __name__ == "__main__":
    # Lightweight smoke run for environments where launching an ASGI server is not needed.
    demo = ChatRequest(session_id="demo-session", user_id="demo-user", message="I have a billing issue with my invoice")
    service = DeterministicSupportService()
    print(service.answer(demo, request_id="demo-request").model_dump_json(indent=2))
