"""Mini-framework pédagogique cumulatif pour l'AI Engineering Bootcamp.

Ce package expose progressivement les composants construits pendant la
Semaine 4 — AI Framework Engineering.

Règle importante :
- les modules restent la source de vérité technique ;
- ce fichier d'initialisation ne remplace jamais les exports précédents ;
- les nouveaux exports sont ajoutés de façon cumulative ;
- en cas de collision de noms entre un module spécialisé et le module
  d'intégration, l'export canonique pointe vers le module spécialisé et
  l'export d'intégration reçoit un alias explicite.

Exemple :
    from mini_framework import ToolRegistry
    from mini_framework import IntegrationToolRegistry
"""

from . import architecture, agent, tool_registry, memory, workflow, observability, integration

from .architecture import (
    ArchitectureBlueprint,
    ComponentSpec,
    DecisionRecord,
    FrameworkArchitect,
    build_default_architecture,
)

from .agent import (
    Agent,
    AgentResult,
    EchoModelClient,
    ModelClient,
    ModelRequest,
    ModelResponse,
    RunContext,
    TraceEvent as AgentTraceEvent,
)

from .tool_registry import (
    ToolContext,
    ToolDefinition,
    ToolExecutionError,
    ToolRegistry,
    ToolRegistryError,
    ToolResult,
    ToolSchemaError,
    build_demo_registry,
    register_decorated,
    tool,
)

from .memory import (
    MemoryQuery,
    MemoryRecord,
    MemorySearchResult,
    MemoryStore,
)

from .workflow import (
    StepResult,
    TraceEvent as WorkflowTraceEvent,
    WorkflowContext,
    WorkflowDefinition,
    WorkflowEngine,
    WorkflowRun,
    WorkflowState,
    WorkflowStep,
    WorkflowValidationError,
)

from .observability import (
    EventRecord,
    MetricPoint,
    Observability,
    ObservabilityConfig,
    SpanRecord,
    TraceRecord,
    summarize_export,
)

from .integration import (
    AgentSpec,
    ApprovalRequired,
    FrameworkError,
    MiniAgentFramework,
    PermissionError,
    RunResult,
    ToolSpec,
    Tracer,
    ValidationError,
    build_support_framework,
)
from .integration import MemoryStore as IntegrationMemoryStore
from .integration import ToolRegistry as IntegrationToolRegistry
from .integration import ToolResult as IntegrationToolResult
from .integration import TraceEvent as IntegrationTraceEvent
from .integration import WorkflowDefinition as IntegrationWorkflowDefinition
from .integration import WorkflowStep as IntegrationWorkflowStep

__all__ = [
    # Modules
    "architecture",
    "agent",
    "tool_registry",
    "memory",
    "workflow",
    "observability",
    "integration",

    # Day 1 — Architecture
    "ArchitectureBlueprint",
    "ComponentSpec",
    "DecisionRecord",
    "FrameworkArchitect",
    "build_default_architecture",

    # Day 2 — Agent abstraction
    "Agent",
    "AgentResult",
    "EchoModelClient",
    "ModelClient",
    "ModelRequest",
    "ModelResponse",
    "RunContext",
    "AgentTraceEvent",

    # Day 3 — Tool registry
    "ToolContext",
    "ToolDefinition",
    "ToolExecutionError",
    "ToolRegistry",
    "ToolRegistryError",
    "ToolResult",
    "ToolSchemaError",
    "build_demo_registry",
    "register_decorated",
    "tool",

    # Day 4 — Memory layer
    "MemoryQuery",
    "MemoryRecord",
    "MemorySearchResult",
    "MemoryStore",

    # Day 5 — Workflow engine
    "StepResult",
    "WorkflowTraceEvent",
    "WorkflowContext",
    "WorkflowDefinition",
    "WorkflowEngine",
    "WorkflowRun",
    "WorkflowState",
    "WorkflowStep",
    "WorkflowValidationError",

    # Day 6 — Observability
    "EventRecord",
    "MetricPoint",
    "Observability",
    "ObservabilityConfig",
    "SpanRecord",
    "TraceRecord",
    "summarize_export",

    # Day 7 — Integration facade
    "AgentSpec",
    "ApprovalRequired",
    "FrameworkError",
    "MiniAgentFramework",
    "PermissionError",
    "RunResult",
    "ToolSpec",
    "Tracer",
    "ValidationError",
    "build_support_framework",
    "IntegrationMemoryStore",
    "IntegrationToolRegistry",
    "IntegrationToolResult",
    "IntegrationTraceEvent",
    "IntegrationWorkflowDefinition",
    "IntegrationWorkflowStep",
]
