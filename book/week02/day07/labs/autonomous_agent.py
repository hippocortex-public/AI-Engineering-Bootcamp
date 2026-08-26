from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
import json
import re
from typing import Any, Callable, Dict, List, Optional


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    BLOCKED = "blocked"
    FAILED = "failed"


class RunStatus(str, Enum):
    RUNNING = "running"
    NEEDS_INPUT = "needs_input"
    COMPLETED = "completed"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass
class ToolResult:
    ok: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    cost: int = 1


@dataclass
class ToolDefinition:
    name: str
    description: str
    handler: Callable[[Dict[str, Any]], ToolResult]
    safe: bool = True


@dataclass
class Task:
    id: str
    name: str
    tool_name: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    observation: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    requires_approval: bool = False


@dataclass
class TraceEvent:
    step: int
    event_type: str
    message: str
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentState:
    user_id: str
    objective: str
    status: RunStatus = RunStatus.RUNNING
    tasks: List[Task] = field(default_factory=list)
    current_step: int = 0
    budget_used: int = 0
    max_budget: int = 12
    missing_inputs: List[str] = field(default_factory=list)
    final_answer: Optional[str] = None
    traces: List[TraceEvent] = field(default_factory=list)

    def add_trace(self, event_type: str, message: str, payload: Optional[Dict[str, Any]] = None) -> None:
        self.traces.append(TraceEvent(self.current_step, event_type, message, payload or {}))

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, payload: str) -> "AgentState":
        raw = json.loads(payload)
        return cls(
            user_id=raw["user_id"],
            objective=raw["objective"],
            status=RunStatus(raw.get("status", RunStatus.RUNNING)),
            tasks=[
                Task(
                    id=t["id"],
                    name=t["name"],
                    tool_name=t["tool_name"],
                    arguments=t.get("arguments", {}),
                    status=TaskStatus(t.get("status", TaskStatus.PENDING)),
                    observation=t.get("observation"),
                    error=t.get("error"),
                    requires_approval=t.get("requires_approval", False),
                )
                for t in raw.get("tasks", [])
            ],
            current_step=raw.get("current_step", 0),
            budget_used=raw.get("budget_used", 0),
            max_budget=raw.get("max_budget", 12),
            missing_inputs=raw.get("missing_inputs", []),
            final_answer=raw.get("final_answer"),
            traces=[
                TraceEvent(
                    step=e["step"],
                    event_type=e["event_type"],
                    message=e["message"],
                    payload=e.get("payload", {}),
                )
                for e in raw.get("traces", [])
            ],
        )


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolDefinition:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name]

    def execute(self, name: str, arguments: Dict[str, Any]) -> ToolResult:
        return self.get(name).handler(arguments)

    def schema(self) -> List[Dict[str, Any]]:
        return [{"name": t.name, "description": t.description, "safe": t.safe} for t in self._tools.values()]


def extract_order_id(text: str) -> Optional[str]:
    match = re.search(r"\b(?:ORDER|CMD)-\d{3,8}\b", text.upper())
    return match.group(0) if match else None


def tool_search_refund_policy(arguments: Dict[str, Any]) -> ToolResult:
    return ToolResult(ok=True, data={
        "policy": "refund_policy",
        "eligible_days": 30,
        "requires_order_id": True,
        "requires_human_approval_for_refund": True,
    }, cost=1)


def tool_check_order(arguments: Dict[str, Any]) -> ToolResult:
    order_id = arguments.get("order_id")
    if not order_id:
        return ToolResult(ok=False, error="order_id is required", cost=1)
    fake_orders = {
        "ORDER-1234": {"status": "delivered", "days_since_delivery": 7, "amount": 49.90},
        "CMD-2024": {"status": "in_transit", "days_since_delivery": None, "amount": 89.00},
        "ORDER-9999": {"status": "delivered", "days_since_delivery": 45, "amount": 19.99},
    }
    if order_id not in fake_orders:
        return ToolResult(ok=False, error="order not found", cost=1)
    return ToolResult(ok=True, data={"order_id": order_id, **fake_orders[order_id]}, cost=1)


def tool_create_support_ticket(arguments: Dict[str, Any]) -> ToolResult:
    order_id = arguments.get("order_id", "UNKNOWN")
    reason = arguments.get("reason", "customer_request")
    return ToolResult(ok=True, data={"ticket_id": f"TICKET-{order_id.replace('-', '')}", "reason": reason}, cost=2)


def tool_issue_refund(arguments: Dict[str, Any]) -> ToolResult:
    order_id = arguments.get("order_id")
    amount = arguments.get("amount")
    if not order_id or amount is None:
        return ToolResult(ok=False, error="order_id and amount are required", cost=2)
    return ToolResult(ok=True, data={"refund_id": f"REFUND-{order_id.replace('-', '')}", "amount": amount}, cost=2)


def tool_draft_response(arguments: Dict[str, Any]) -> ToolResult:
    status = arguments.get("status", "processed")
    ticket_id = arguments.get("ticket_id")
    order_id = arguments.get("order_id", "votre commande")
    if ticket_id:
        message = f"Votre demande concernant {order_id} est prise en charge. Le ticket {ticket_id} a été créé avec le statut '{status}'."
    else:
        message = f"Votre demande concernant {order_id} a été analysée avec le statut '{status}'."
    return ToolResult(ok=True, data={"message": message}, cost=1)


def build_default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(ToolDefinition("search_refund_policy", "Récupère la politique de remboursement.", tool_search_refund_policy, True))
    registry.register(ToolDefinition("check_order", "Vérifie le statut d'une commande.", tool_check_order, True))
    registry.register(ToolDefinition("create_support_ticket", "Crée un ticket support non destructif.", tool_create_support_ticket, True))
    registry.register(ToolDefinition("issue_refund", "Déclenche un remboursement. Action sensible.", tool_issue_refund, False))
    registry.register(ToolDefinition("draft_response", "Prépare une réponse finale orientée utilisateur.", tool_draft_response, True))
    return registry


class AutonomousSupportAgent:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def start(self, user_id: str, objective: str, max_budget: int = 12) -> AgentState:
        state = AgentState(user_id=user_id, objective=objective, max_budget=max_budget)
        state.add_trace("objective_received", "Objective received", {"objective": objective})
        if not objective or len(objective.strip()) < 8:
            state.status = RunStatus.NEEDS_INPUT
            state.missing_inputs.append("objective_detail")
            state.add_trace("clarification_required", "Objective is too vague")
            return state

        order_id = extract_order_id(objective)
        lowered = objective.lower()
        is_refund = any(word in lowered for word in ["refund", "rembourse", "remboursement"])
        is_ticket = any(word in lowered for word in ["ticket", "support", "incident"])

        if is_refund and not order_id:
            state.status = RunStatus.NEEDS_INPUT
            state.missing_inputs.append("order_id")
            state.add_trace("clarification_required", "Refund objective requires an order id")
            return state

        state.tasks = self._plan(order_id, is_refund, is_ticket)
        state.add_trace("plan_created", "Plan created", {"task_count": len(state.tasks)})
        return state

    def _plan(self, order_id: Optional[str], is_refund: bool, is_ticket: bool) -> List[Task]:
        if is_refund:
            return [
                Task("T1", "Lire la politique de remboursement", "search_refund_policy"),
                Task("T2", "Vérifier la commande", "check_order", {"order_id": order_id}),
                Task("T3", "Créer un ticket de suivi", "create_support_ticket", {"order_id": order_id, "reason": "refund_request"}),
                Task("T4", "Préparer un remboursement potentiel", "issue_refund", {"order_id": order_id}, requires_approval=True),
                Task("T5", "Rédiger la réponse finale", "draft_response", {"order_id": order_id, "status": "refund_review"}),
            ]
        if is_ticket:
            return [
                Task("T1", "Créer un ticket support", "create_support_ticket", {"reason": "support_request"}),
                Task("T2", "Rédiger la réponse finale", "draft_response", {"status": "ticket_created"}),
            ]
        return [Task("T1", "Rédiger une réponse de clarification", "draft_response", {"status": "needs_scope"})]

    def run(self, state: AgentState, max_steps: int = 10, approve_sensitive_actions: bool = False) -> AgentState:
        while state.status == RunStatus.RUNNING and state.current_step < max_steps:
            task = next((t for t in state.tasks if t.status == TaskStatus.PENDING), None)
            if task is None:
                state.status = RunStatus.COMPLETED
                state.final_answer = self._compose_final_answer(state)
                state.add_trace("run_completed", "All tasks completed")
                return state
            self.step(state, task, approve_sensitive_actions)
        if state.status == RunStatus.RUNNING:
            state.status = RunStatus.STOPPED
            state.add_trace("max_steps_reached", "Run stopped by max step guardrail", {"max_steps": max_steps})
        return state

    def step(self, state: AgentState, task: Task, approve_sensitive_actions: bool = False) -> None:
        state.current_step += 1
        state.add_trace("task_started", f"Starting task {task.id}", {"tool": task.tool_name})
        tool = self.registry.get(task.tool_name)

        if state.budget_used >= state.max_budget:
            task.status = TaskStatus.BLOCKED
            task.error = "budget_exceeded"
            state.status = RunStatus.STOPPED
            state.add_trace("budget_exceeded", "Budget guardrail stopped the run")
            return

        if not tool.safe and not approve_sensitive_actions:
            task.status = TaskStatus.BLOCKED
            task.error = "human_approval_required"
            state.status = RunStatus.NEEDS_INPUT
            state.missing_inputs.append(f"approval_for_{task.tool_name}")
            state.add_trace("approval_required", "Sensitive action requires human approval", {"tool": task.tool_name})
            return

        args = self._enrich_arguments_from_state(state, task)
        result = self.registry.execute(task.tool_name, args)
        state.budget_used += result.cost

        if not result.ok:
            task.status = TaskStatus.FAILED
            task.error = result.error
            state.status = RunStatus.FAILED
            state.add_trace("task_failed", f"Task {task.id} failed", {"error": result.error})
            return

        task.status = TaskStatus.DONE
        task.arguments = args
        task.observation = result.data
        state.add_trace("task_completed", f"Task {task.id} completed", {"observation": result.data})

    def _enrich_arguments_from_state(self, state: AgentState, task: Task) -> Dict[str, Any]:
        args = dict(task.arguments)
        if task.tool_name == "issue_refund":
            order_task = next((t for t in state.tasks if t.tool_name == "check_order" and t.observation), None)
            if order_task:
                days = order_task.observation.get("days_since_delivery")
                amount = order_task.observation.get("amount")
                args["amount"] = amount if days is not None and days <= 30 else 0
        if task.tool_name == "draft_response":
            ticket = next((t for t in state.tasks if t.tool_name == "create_support_ticket" and t.observation), None)
            if ticket:
                args["ticket_id"] = ticket.observation.get("ticket_id")
            refund = next((t for t in state.tasks if t.tool_name == "issue_refund" and t.observation), None)
            if refund:
                args["status"] = "refund_issued"
            elif any(t.status == TaskStatus.BLOCKED for t in state.tasks):
                args["status"] = "requires_human_approval"
        return args

    def _compose_final_answer(self, state: AgentState) -> str:
        response_task = next((t for t in reversed(state.tasks) if t.tool_name == "draft_response" and t.observation), None)
        if response_task:
            return response_task.observation["message"]
        return "La demande a été traitée, mais aucune réponse finale n'a été générée."


def demo() -> None:
    agent = AutonomousSupportAgent(build_default_registry())
    state = agent.start("user-1", "Je veux un remboursement pour ORDER-1234", max_budget=12)
    state = agent.run(state, approve_sensitive_actions=False)
    print("Status:", state.status.value)
    print("Missing inputs:", state.missing_inputs)
    print("Budget used:", state.budget_used)
    print("Trace events:", len(state.traces))


if __name__ == "__main__":
    demo()
