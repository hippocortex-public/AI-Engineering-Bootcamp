"""Integration layer for a pedagogical AI agent mini-framework.

The module intentionally uses only the Python standard library. It models the
core contracts needed to integrate agents, tools, memory, workflow execution and
observability in a deterministic way.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional
import json
import time


class FrameworkError(Exception):
    """Base exception for framework errors."""


class ValidationError(FrameworkError):
    """Raised when a local contract validation fails."""


class PermissionError(FrameworkError):
    """Raised when an agent is not allowed to call a tool."""


class ApprovalRequired(FrameworkError):
    """Raised when a sensitive tool is requested without approval."""


@dataclass(frozen=True)
class AgentSpec:
    """Declarative contract for an agent."""

    name: str
    instructions: str
    allowed_tools: List[str]

    def validate(self) -> None:
        if not self.name:
            raise ValidationError("Agent name is required.")
        if not self.instructions:
            raise ValidationError("Agent instructions are required.")
        if len(set(self.allowed_tools)) != len(self.allowed_tools):
            raise ValidationError("Agent allowed_tools contains duplicates.")


@dataclass
class ToolResult:
    """Structured result returned by a tool."""

    ok: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"ok": self.ok, "data": self.data, "error": self.error}


@dataclass(frozen=True)
class ToolSpec:
    """Declarative contract for a tool."""

    name: str
    description: str
    input_schema: Dict[str, Any]
    handler: Callable[[Dict[str, Any]], Dict[str, Any]]
    requires_approval: bool = False

    def validate_args(self, arguments: Dict[str, Any]) -> None:
        if not isinstance(arguments, dict):
            raise ValidationError(f"Arguments for tool '{self.name}' must be a dict.")

        required = self.input_schema.get("required", [])
        properties = self.input_schema.get("properties", {})

        for key in required:
            if key not in arguments:
                raise ValidationError(f"Missing required argument '{key}' for tool '{self.name}'.")

        additional_allowed = self.input_schema.get("additionalProperties", True)
        if not additional_allowed:
            unexpected = set(arguments) - set(properties)
            if unexpected:
                names = ", ".join(sorted(unexpected))
                raise ValidationError(f"Unexpected argument(s) for tool '{self.name}': {names}.")

        for key, spec in properties.items():
            if key not in arguments:
                continue
            expected_type = spec.get("type")
            value = arguments[key]
            if expected_type == "string" and not isinstance(value, str):
                raise ValidationError(f"Argument '{key}' must be a string.")
            if expected_type == "number" and not isinstance(value, (int, float)):
                raise ValidationError(f"Argument '{key}' must be a number.")
            if expected_type == "boolean" and not isinstance(value, bool):
                raise ValidationError(f"Argument '{key}' must be a boolean.")


@dataclass
class TraceEvent:
    """One observability event."""

    name: str
    payload: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "payload": self.payload, "timestamp": self.timestamp}


class Tracer:
    """Small event tracer for deterministic labs."""

    def __init__(self) -> None:
        self.events: List[TraceEvent] = []

    def record(self, name: str, **payload: Any) -> None:
        safe_payload = {}
        for key, value in payload.items():
            if "secret" in key.lower() or "token" in key.lower():
                safe_payload[key] = "[REDACTED]"
            else:
                safe_payload[key] = value
        self.events.append(TraceEvent(name=name, payload=safe_payload))

    def export(self) -> List[Dict[str, Any]]:
        return [event.to_dict() for event in self.events]

    def names(self) -> List[str]:
        return [event.name for event in self.events]


class MemoryStore:
    """Simple user-scoped memory store."""

    def __init__(self) -> None:
        self._records: Dict[str, Dict[str, Any]] = {}

    def remember(self, user_id: str, key: str, value: Any) -> None:
        if not user_id:
            raise ValidationError("user_id is required.")
        if not key:
            raise ValidationError("memory key is required.")
        self._records.setdefault(user_id, {})[key] = value

    def retrieve(self, user_id: str) -> Dict[str, Any]:
        return dict(self._records.get(user_id, {}))

    def forget(self, user_id: str, key: Optional[str] = None) -> None:
        if key is None:
            self._records.pop(user_id, None)
        elif user_id in self._records:
            self._records[user_id].pop(key, None)


class ToolRegistry:
    """Controlled registry for tool execution."""

    def __init__(self, tracer: Optional[Tracer] = None) -> None:
        self._tools: Dict[str, ToolSpec] = {}
        self.tracer = tracer or Tracer()

    def register(self, tool: ToolSpec) -> None:
        if not tool.name:
            raise ValidationError("Tool name is required.")
        if tool.name in self._tools:
            raise ValidationError(f"Tool '{tool.name}' is already registered.")
        self._tools[tool.name] = tool
        self.tracer.record("tool.registered", tool=tool.name, sensitive=tool.requires_approval)

    def list_tools(self) -> List[str]:
        return sorted(self._tools)

    def get(self, name: str) -> ToolSpec:
        if name not in self._tools:
            raise ValidationError(f"Unknown tool '{name}'.")
        return self._tools[name]

    def call(
        self,
        *,
        tool_name: str,
        arguments: Dict[str, Any],
        agent: AgentSpec,
        approval: bool = False,
    ) -> ToolResult:
        tool = self.get(tool_name)

        if tool_name not in agent.allowed_tools:
            self.tracer.record("tool.denied", agent=agent.name, tool=tool_name, reason="not_allowed")
            raise PermissionError(f"Agent '{agent.name}' is not allowed to call tool '{tool_name}'.")

        if tool.requires_approval and not approval:
            self.tracer.record("tool.blocked", agent=agent.name, tool=tool_name, reason="approval_required")
            raise ApprovalRequired(f"Tool '{tool_name}' requires approval.")

        tool.validate_args(arguments)

        self.tracer.record("tool.call.started", agent=agent.name, tool=tool_name)
        try:
            data = tool.handler(arguments)
        except Exception as exc:  # pragma: no cover - defensive branch
            self.tracer.record("tool.call.failed", agent=agent.name, tool=tool_name, error=str(exc))
            return ToolResult(ok=False, error=str(exc))
        self.tracer.record("tool.call.completed", agent=agent.name, tool=tool_name)
        return ToolResult(ok=True, data=data)


@dataclass(frozen=True)
class WorkflowStep:
    """One deterministic workflow step."""

    name: str
    agent_name: str
    tool_name: str
    argument_keys: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class WorkflowDefinition:
    """Declarative workflow definition."""

    name: str
    steps: List[WorkflowStep]

    def validate(self) -> None:
        if not self.name:
            raise ValidationError("Workflow name is required.")
        names = [step.name for step in self.steps]
        if len(names) != len(set(names)):
            raise ValidationError("Workflow contains duplicate step names.")

        known = set(names)
        for step in self.steps:
            for dep in step.depends_on:
                if dep not in known:
                    raise ValidationError(f"Step '{step.name}' depends on unknown step '{dep}'.")

        self._assert_acyclic()

    def _assert_acyclic(self) -> None:
        graph = {step.name: list(step.depends_on) for step in self.steps}
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node: str) -> None:
            if node in visiting:
                raise ValidationError("Workflow contains a dependency cycle.")
            if node in visited:
                return
            visiting.add(node)
            for dep in graph[node]:
                visit(dep)
            visiting.remove(node)
            visited.add(node)

        for name in graph:
            visit(name)

    def ordered_steps(self) -> List[WorkflowStep]:
        self.validate()
        remaining = {step.name: step for step in self.steps}
        completed: set[str] = set()
        ordered: List[WorkflowStep] = []

        while remaining:
            ready = [
                step
                for step in remaining.values()
                if all(dep in completed for dep in step.depends_on)
            ]
            if not ready:
                raise ValidationError("No executable workflow step found.")
            ready.sort(key=lambda item: item.name)
            step = ready[0]
            ordered.append(step)
            completed.add(step.name)
            remaining.pop(step.name)
        return ordered


@dataclass
class RunResult:
    """Structured result returned by the integrated framework."""

    status: str
    summary: str
    outputs: Dict[str, Any]
    blocked_actions: List[str]
    memory_used: List[str]
    trace: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "summary": self.summary,
            "outputs": self.outputs,
            "blocked_actions": self.blocked_actions,
            "memory_used": self.memory_used,
            "trace": self.trace,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)


class MiniAgentFramework:
    """Integrated facade used by the lab."""

    def __init__(self) -> None:
        self.tracer = Tracer()
        self.memory = MemoryStore()
        self.tools = ToolRegistry(tracer=self.tracer)
        self.agents: Dict[str, AgentSpec] = {}
        self.workflows: Dict[str, WorkflowDefinition] = {}

    def register_agent(self, agent: AgentSpec) -> None:
        agent.validate()
        if agent.name in self.agents:
            raise ValidationError(f"Agent '{agent.name}' is already registered.")
        self.agents[agent.name] = agent
        self.tracer.record("agent.registered", agent=agent.name)

    def register_tool(self, tool: ToolSpec) -> None:
        self.tools.register(tool)

    def register_workflow(self, workflow: WorkflowDefinition) -> None:
        workflow.validate()
        if workflow.name in self.workflows:
            raise ValidationError(f"Workflow '{workflow.name}' is already registered.")
        self.workflows[workflow.name] = workflow
        self.tracer.record("workflow.registered", workflow=workflow.name)

    def _build_arguments(
        self,
        *,
        step: WorkflowStep,
        message: str,
        user_id: str,
        memory: Dict[str, Any],
        outputs: Dict[str, Any],
    ) -> Dict[str, Any]:
        context: Dict[str, Any] = {
            "message": message,
            "user_id": user_id,
            "memory": memory,
            "outputs": outputs,
        }
        arguments = {}
        for key in step.argument_keys:
            if key in context:
                arguments[key] = context[key]
            elif key in outputs:
                arguments[key] = outputs[key]
            else:
                arguments[key] = None
        return arguments

    def run(
        self,
        *,
        user_id: str,
        message: str,
        workflow_name: str,
        approval: bool = False,
    ) -> RunResult:
        self.tracer.record("run.started", workflow=workflow_name, user_id=user_id)
        outputs: Dict[str, Any] = {}
        blocked: List[str] = []
        memory = self.memory.retrieve(user_id)
        memory_used = sorted(memory.keys())
        self.tracer.record("memory.retrieved", user_id=user_id, keys=memory_used)

        if workflow_name not in self.workflows:
            self.tracer.record("run.failed", reason="unknown_workflow", workflow=workflow_name)
            return RunResult(
                status="failed",
                summary=f"Unknown workflow '{workflow_name}'.",
                outputs=outputs,
                blocked_actions=blocked,
                memory_used=memory_used,
                trace=self.tracer.export(),
            )

        workflow = self.workflows[workflow_name]

        try:
            ordered_steps = workflow.ordered_steps()
        except ValidationError as exc:
            self.tracer.record("run.failed", reason="invalid_workflow", error=str(exc))
            return RunResult(
                status="failed",
                summary=str(exc),
                outputs=outputs,
                blocked_actions=blocked,
                memory_used=memory_used,
                trace=self.tracer.export(),
            )

        status = "completed"
        summary = "Workflow completed."

        for step in ordered_steps:
            if step.agent_name not in self.agents:
                status = "failed"
                summary = f"Unknown agent '{step.agent_name}'."
                self.tracer.record("run.failed", reason="unknown_agent", agent=step.agent_name)
                break

            agent = self.agents[step.agent_name]
            arguments = self._build_arguments(
                step=step,
                message=message,
                user_id=user_id,
                memory=memory,
                outputs=outputs,
            )

            self.tracer.record("workflow.step.started", step=step.name, tool=step.tool_name)
            try:
                result = self.tools.call(
                    tool_name=step.tool_name,
                    arguments=arguments,
                    agent=agent,
                    approval=approval,
                )
            except ApprovalRequired:
                status = "blocked"
                blocked.append(step.tool_name)
                summary = f"Workflow blocked: approval required for '{step.tool_name}'."
                self.tracer.record("workflow.step.blocked", step=step.name, tool=step.tool_name)
                break
            except FrameworkError as exc:
                status = "failed"
                summary = str(exc)
                self.tracer.record("workflow.step.failed", step=step.name, error=str(exc))
                break

            if not result.ok:
                status = "failed"
                summary = result.error or f"Tool '{step.tool_name}' failed."
                self.tracer.record("workflow.step.failed", step=step.name, error=summary)
                break

            outputs[step.name] = result.data
            self.tracer.record("workflow.step.completed", step=step.name)

        self.tracer.record("run.completed", status=status)
        return RunResult(
            status=status,
            summary=summary,
            outputs=outputs,
            blocked_actions=blocked,
            memory_used=memory_used,
            trace=self.tracer.export(),
        )


def _string_schema(*required: str) -> Dict[str, Any]:
    return {
        "type": "object",
        "required": list(required),
        "properties": {key: {"type": "string"} for key in required},
        "additionalProperties": False,
    }


def _mixed_schema(required: Iterable[str], properties: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    return {
        "type": "object",
        "required": list(required),
        "properties": properties,
        "additionalProperties": False,
    }


def build_support_framework() -> MiniAgentFramework:
    """Build a deterministic support assistant framework used in the lab."""

    framework = MiniAgentFramework()

    def classify_ticket(args: Dict[str, Any]) -> Dict[str, Any]:
        message = args["message"].lower()
        if "remboursement" in message or "refund" in message:
            category = "refund_request"
            risk = "medium"
        elif "cass" in message or "broken" in message:
            category = "damaged_order"
            risk = "medium"
        else:
            category = "general_support"
            risk = "low"
        return {"category": category, "risk": risk}

    def search_kb(args: Dict[str, Any]) -> Dict[str, Any]:
        outputs = args["outputs"]
        category = outputs.get("classify", {}).get("category", "general_support")
        policy = {
            "refund_request": "Refunds require order verification and human approval.",
            "damaged_order": "Damaged orders can be replaced after evidence review.",
            "general_support": "Ask a clarifying question and provide standard support guidance.",
        }[category]
        return {"policy": policy, "source": "support_policy_v1"}

    def draft_answer(args: Dict[str, Any]) -> Dict[str, Any]:
        memory = args.get("memory", {})
        tone = memory.get("preferred_tone", "professionnel")
        message = args["message"]
        policy = args["outputs"].get("search_policy", {}).get("policy", "Nous allons vérifier votre demande.")
        return {
            "draft": (
                f"Ton {tone}. Nous avons bien reçu votre demande : '{message}'. "
                f"Politique applicable : {policy}"
            )
        }

    def issue_refund(args: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "refund_prepared": True,
            "amount": args["amount"],
            "note": "Refund action executed only because approval=True.",
        }

    framework.register_tool(
        ToolSpec(
            name="classify_ticket",
            description="Classify a customer support message.",
            input_schema=_string_schema("message"),
            handler=classify_ticket,
        )
    )
    framework.register_tool(
        ToolSpec(
            name="search_kb",
            description="Retrieve an internal support policy.",
            input_schema=_mixed_schema(
                required=["outputs"],
                properties={"outputs": {"type": "object"}},
            ),
            handler=search_kb,
        )
    )
    framework.register_tool(
        ToolSpec(
            name="draft_answer",
            description="Draft a customer-facing answer.",
            input_schema=_mixed_schema(
                required=["message", "memory", "outputs"],
                properties={
                    "message": {"type": "string"},
                    "memory": {"type": "object"},
                    "outputs": {"type": "object"},
                },
            ),
            handler=draft_answer,
        )
    )
    framework.register_tool(
        ToolSpec(
            name="issue_refund",
            description="Sensitive financial action.",
            input_schema={
                "type": "object",
                "required": ["amount"],
                "properties": {"amount": {"type": "number"}},
                "additionalProperties": False,
            },
            handler=issue_refund,
            requires_approval=True,
        )
    )

    framework.register_agent(
        AgentSpec(
            name="support_agent",
            instructions="Resolve customer support requests with policy-grounded answers.",
            allowed_tools=["classify_ticket", "search_kb", "draft_answer", "issue_refund"],
        )
    )

    framework.register_workflow(
        WorkflowDefinition(
            name="support_resolution",
            steps=[
                WorkflowStep(
                    name="classify",
                    agent_name="support_agent",
                    tool_name="classify_ticket",
                    argument_keys=["message"],
                ),
                WorkflowStep(
                    name="search_policy",
                    agent_name="support_agent",
                    tool_name="search_kb",
                    argument_keys=["outputs"],
                    depends_on=["classify"],
                ),
                WorkflowStep(
                    name="draft",
                    agent_name="support_agent",
                    tool_name="draft_answer",
                    argument_keys=["message", "memory", "outputs"],
                    depends_on=["search_policy"],
                ),
            ],
        )
    )

    framework.register_workflow(
        WorkflowDefinition(
            name="support_refund_with_approval",
            steps=[
                WorkflowStep(
                    name="classify",
                    agent_name="support_agent",
                    tool_name="classify_ticket",
                    argument_keys=["message"],
                ),
                WorkflowStep(
                    name="search_policy",
                    agent_name="support_agent",
                    tool_name="search_kb",
                    argument_keys=["outputs"],
                    depends_on=["classify"],
                ),
                WorkflowStep(
                    name="draft",
                    agent_name="support_agent",
                    tool_name="draft_answer",
                    argument_keys=["message", "memory", "outputs"],
                    depends_on=["search_policy"],
                ),
                WorkflowStep(
                    name="refund",
                    agent_name="support_agent",
                    tool_name="issue_refund",
                    argument_keys=["amount"],
                    depends_on=["draft"],
                ),
            ],
        )
    )

    return framework
