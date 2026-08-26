"""Validation du fichier mini_framework/__init__.py cumulatif.

Ce test garantit que l'installation du jour 7 ne masque pas les composants
construits pendant les jours précédents de la semaine 4.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mini_framework as mf


EXPECTED_PUBLIC_API = [
    # J1
    "ArchitectureBlueprint",
    "ComponentSpec",
    "DecisionRecord",
    "FrameworkArchitect",
    "build_default_architecture",
    # J2
    "Agent",
    "AgentResult",
    "EchoModelClient",
    "ModelClient",
    "ModelRequest",
    "ModelResponse",
    "RunContext",
    "AgentTraceEvent",
    # J3
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
    # J4
    "MemoryQuery",
    "MemoryRecord",
    "MemorySearchResult",
    "MemoryStore",
    # J5
    "StepResult",
    "WorkflowTraceEvent",
    "WorkflowContext",
    "WorkflowDefinition",
    "WorkflowEngine",
    "WorkflowRun",
    "WorkflowState",
    "WorkflowStep",
    "WorkflowValidationError",
    # J6
    "EventRecord",
    "MetricPoint",
    "Observability",
    "ObservabilityConfig",
    "SpanRecord",
    "TraceRecord",
    "summarize_export",
    # J7
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


def test_public_api_is_cumulative():
    missing = [name for name in EXPECTED_PUBLIC_API if not hasattr(mf, name)]
    assert missing == [], f"Exports manquants dans mini_framework.__init__: {missing}"


def test_canonical_exports_do_not_point_to_integration_duplicates():
    assert mf.ToolRegistry is mf.tool_registry.ToolRegistry
    assert mf.ToolResult is mf.tool_registry.ToolResult
    assert mf.MemoryStore is mf.memory.MemoryStore
    assert mf.WorkflowDefinition is mf.workflow.WorkflowDefinition
    assert mf.WorkflowStep is mf.workflow.WorkflowStep


def test_integration_duplicates_are_available_with_explicit_aliases():
    assert mf.IntegrationToolRegistry is mf.integration.ToolRegistry
    assert mf.IntegrationToolResult is mf.integration.ToolResult
    assert mf.IntegrationMemoryStore is mf.integration.MemoryStore
    assert mf.IntegrationWorkflowDefinition is mf.integration.WorkflowDefinition
    assert mf.IntegrationWorkflowStep is mf.integration.WorkflowStep


if __name__ == "__main__":
    test_public_api_is_cumulative()
    test_canonical_exports_do_not_point_to_integration_duplicates()
    test_integration_duplicates_are_available_with_explicit_aliases()
    print("3 tests passed")
