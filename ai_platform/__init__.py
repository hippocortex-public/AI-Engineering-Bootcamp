"""
AI platform package for Week 5.

The initializer is cumulative by design: each new module must add exports
without removing public symbols introduced by earlier days.
"""

from .architecture import (
    ArchitectureBlueprint,
    ArchitectureComponent,
    ProductionArchitectureValidator,
    ProductionControl,
    ReadinessReport,
    Risk,
    build_support_ai_blueprint,
    load_blueprint_from_dict,
    render_mermaid,
    summarize_readiness,
)

from .api import (
    APISettings,
    ChatRequest,
    ChatResponse,
    DeterministicSupportService,
    ErrorResponse,
    InMemoryRateLimiter,
    RateLimitDecision,
    SessionTranscript,
    build_router,
    create_app,
)

__all__ = [
    # Week 5 Day 1 — Architecture production
    "ArchitectureBlueprint",
    "ArchitectureComponent",
    "ProductionArchitectureValidator",
    "ProductionControl",
    "ReadinessReport",
    "Risk",
    "build_support_ai_blueprint",
    "load_blueprint_from_dict",
    "render_mermaid",
    "summarize_readiness",
    # Week 5 Day 2 — API FastAPI
    "APISettings",
    "ChatRequest",
    "ChatResponse",
    "DeterministicSupportService",
    "ErrorResponse",
    "InMemoryRateLimiter",
    "RateLimitDecision",
    "SessionTranscript",
    "build_router",
    "create_app",
]
