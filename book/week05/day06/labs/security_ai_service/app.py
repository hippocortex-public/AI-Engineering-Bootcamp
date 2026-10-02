import json
import logging
from typing import Annotated
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Request, Security
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import ValidationError

from .auth import IdentityStore, Principal
from .policy import AccessDenied, Document, DocumentStore, ResourceNotFound, ToolPolicy, require_scope
from .quota import FixedWindowLimiter, QuotaExceeded
from .schemas import ChatRequest, ReadDocumentArguments, ToolRequest

logger = logging.getLogger("security_ai_service.audit")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def simulate_answer(message: str, document: Document | None) -> str:
    """Simulation : aucune exécution d'outils ou de contenu du document."""
    if document is not None:
        return f"Document autorisé : {document.document_id}. Extrait : {document.text[:200]}"
    return "La sécurité est appliquée par le backend indépendamment du contenu du prompt."


def create_app(identities: IdentityStore | None = None, documents: DocumentStore | None = None,
               limiter: FixedWindowLimiter | None = None) -> FastAPI:
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    identities = identities if identities is not None else IdentityStore.from_environment()
    documents = documents if documents is not None else DocumentStore([
        Document("alpha-guide", "alpha", "Guide interne du tenant alpha."),
        Document("beta-guide", "beta", "Information confidentielle du tenant beta."),
    ])
    limiter = limiter if limiter is not None else FixedWindowLimiter()
    tool_policy = ToolPolicy()
    app = FastAPI(title="Security AI Service Lab", docs_url=None, redoc_url=None, openapi_url=None)

    @app.middleware("http")
    async def audit(request: Request, call_next):
        request.state.request_id = f"req_{uuid4().hex}"
        status = 500
        try:
            response = await call_next(request)
            status = response.status_code
            response.headers["X-Request-ID"] = request.state.request_id
            response.headers["Cache-Control"] = "no-store"
            response.headers["X-Content-Type-Options"] = "nosniff"
            return response
        finally:
            principal = getattr(request.state, "principal", None)
            route = request.scope.get("route")
            logger.info(json.dumps({
                "event": "security_request",
                "request_id": request.state.request_id,
                "route": getattr(route, "path", "unmatched"),
                "status_code": status,
                "subject": principal.subject if principal else "anonymous",
                "tenant": principal.tenant if principal else None,
            }))

    def failure(request: Request, status: int, code: str, headers: dict | None = None) -> JSONResponse:
        return JSONResponse(status_code=status, content={
            "error": code, "request_id": request.state.request_id,
        }, headers=headers)

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request: Request, exc: RequestValidationError):
        # Les erreurs Pydantic par défaut peuvent reproduire l'entrée reçue.
        return failure(request, 422, "invalid_request")

    @app.exception_handler(AccessDenied)
    async def denied(request: Request, exc: AccessDenied):
        return failure(request, 403, "forbidden")

    @app.exception_handler(ResourceNotFound)
    async def not_found(request: Request, exc: ResourceNotFound):
        return failure(request, 404, "not_found")

    @app.exception_handler(QuotaExceeded)
    async def quota_exceeded(request: Request, exc: QuotaExceeded):
        return failure(request, 429, "quota_exceeded", {"Retry-After": str(exc.retry_after)})

    @app.exception_handler(Exception)
    async def internal_error(request: Request, exc: Exception):
        return failure(request, 500, "internal_error", {
            "X-Request-ID": request.state.request_id,
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff",
        })

    def authenticate(request: Request, key: Annotated[str | None, Security(api_key_header)]) -> Principal:
        principal = identities.authenticate(key)
        if principal is None:
            raise HTTPException(401, "unauthorized", headers={"WWW-Authenticate": "APIKey"})
        request.state.principal = principal
        return principal

    def protected(scope: str):
        def check(principal: Annotated[Principal, Depends(authenticate)]) -> Principal:
            require_scope(principal, scope)
            # Toutes les routes protégées partagent le quota de cette identité.
            limiter.consume(principal)
            return principal
        return check

    @app.get("/health")
    def health():
        return {"status": "ok", "provider": "simulated"}

    @app.get("/documents/{document_id}")
    def read_document(document_id: str, principal: Annotated[Principal, Depends(protected("documents:read"))]):
        document = documents.get(principal, document_id)
        return {"document_id": document.document_id, "text": document.text}

    @app.post("/chat")
    def chat(payload: ChatRequest, principal: Annotated[Principal, Depends(protected("chat:write"))]):
        document = documents.get(principal, payload.document_id) if payload.document_id else None
        return {"answer": simulate_answer(payload.message, document), "provider": "simulated"}

    @app.post("/tools/invoke")
    def invoke(payload: ToolRequest, principal: Annotated[Principal, Depends(protected("tools:read"))]):
        tool_policy.authorize(principal, payload.name)
        try:
            arguments = ReadDocumentArguments.model_validate(payload.arguments)
        except ValidationError:
            raise HTTPException(422, "invalid_tool_arguments") from None
        document = documents.get(principal, arguments.document_id)
        return {"tool": "read_document", "result": {"document_id": document.document_id, "text": document.text}}

    return app
