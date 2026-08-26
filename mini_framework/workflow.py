"""
Mini-framework pédagogique — Workflow Engine.

Ce module est volontairement autonome et basé uniquement sur la standard
library Python. Il montre les primitives minimales d'un moteur de workflow
agentique : définition d'étapes, validation de graphe, exécution déterministe,
gestion d'état, retries, garde-fous, approbation humaine et traces.

Le moteur ne remplace pas un orchestrateur de production. Il sert de socle
didactique pour comprendre les responsabilités d'un workflow engine dans un
framework d'agents.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Set
import json
import time
import uuid


JsonDict = Dict[str, Any]
StepHandler = Callable[["WorkflowContext"], Any]
ConditionHandler = Callable[["WorkflowState"], bool]


TERMINAL_STATUSES = {"completed", "failed", "blocked", "skipped"}


@dataclass(frozen=True)
class WorkflowStep:
    """Décrit une étape de workflow.

    Attributes:
        name: Identifiant unique de l'étape.
        handler: Nom du handler enregistré dans le moteur.
        depends_on: Étapes qui doivent être terminées avant celle-ci.
        max_retries: Nombre de tentatives supplémentaires après le premier échec.
        sensitive: Si vrai, l'étape requiert une approbation humaine.
        condition: Nom d'une condition enregistrée. Si fausse, l'étape est skipped.
        timeout_seconds: Champ de design conservé pour expliciter le contrat.
            Le lab ne lance pas de threads ni de signaux ; il trace la valeur.
    """

    name: str
    handler: str
    depends_on: Sequence[str] = field(default_factory=tuple)
    max_retries: int = 0
    sensitive: bool = False
    condition: Optional[str] = None
    timeout_seconds: Optional[float] = None

    def __post_init__(self) -> None:
        if not self.name or not isinstance(self.name, str):
            raise ValueError("step.name must be a non-empty string")
        if not self.handler or not isinstance(self.handler, str):
            raise ValueError("step.handler must be a non-empty string")
        if self.max_retries < 0:
            raise ValueError("step.max_retries must be >= 0")
        if self.timeout_seconds is not None and self.timeout_seconds <= 0:
            raise ValueError("step.timeout_seconds must be positive")


@dataclass(frozen=True)
class WorkflowDefinition:
    """Contrat statique d'un workflow."""

    name: str
    version: str
    steps: Sequence[WorkflowStep]
    description: str = ""

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("workflow.name must be non-empty")
        if not self.version:
            raise ValueError("workflow.version must be non-empty")
        if not self.steps:
            raise ValueError("workflow.steps must not be empty")


@dataclass
class WorkflowState:
    """État mutable partagé pendant une exécution."""

    run_id: str
    input: JsonDict
    data: JsonDict = field(default_factory=dict)
    approvals: Set[str] = field(default_factory=set)
    status: str = "pending"

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value

    def approve(self, step_name: str) -> None:
        self.approvals.add(step_name)

    def to_json(self) -> str:
        payload = {
            "run_id": self.run_id,
            "input": self.input,
            "data": self.data,
            "approvals": sorted(self.approvals),
            "status": self.status,
        }
        return json.dumps(payload, indent=2, sort_keys=True)


@dataclass
class WorkflowContext:
    """Contexte fourni à chaque handler."""

    workflow_name: str
    step_name: str
    attempt: int
    state: WorkflowState

    @property
    def input(self) -> JsonDict:
        return self.state.input

    @property
    def data(self) -> JsonDict:
        return self.state.data


@dataclass
class StepResult:
    """Résultat normalisé d'une étape."""

    name: str
    status: str
    attempts: int
    output: Any = None
    error: Optional[str] = None

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class TraceEvent:
    """Événement d'observabilité simple."""

    run_id: str
    workflow: str
    step: Optional[str]
    event: str
    timestamp: float
    payload: JsonDict = field(default_factory=dict)

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class WorkflowRun:
    """Résultat d'exécution complet."""

    run_id: str
    workflow: str
    status: str
    step_results: Dict[str, StepResult]
    state: WorkflowState
    trace: List[TraceEvent]

    def to_dict(self) -> JsonDict:
        return {
            "run_id": self.run_id,
            "workflow": self.workflow,
            "status": self.status,
            "step_results": {k: v.to_dict() for k, v in self.step_results.items()},
            "state": json.loads(self.state.to_json()),
            "trace": [e.to_dict() for e in self.trace],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)


class WorkflowValidationError(ValueError):
    """Erreur de définition de workflow."""


class WorkflowEngine:
    """Moteur déterministe de workflows.

    Le moteur est volontairement synchrone et simple :
    - le graphe est validé avant exécution ;
    - l'ordre est topologique ;
    - une étape sensible est bloquée sans approbation explicite ;
    - les handlers sont injectés par registre ;
    - les erreurs sont tracées et peuvent déclencher des retries.
    """

    def __init__(self) -> None:
        self._handlers: Dict[str, StepHandler] = {}
        self._conditions: Dict[str, ConditionHandler] = {}

    def register_handler(self, name: str, handler: StepHandler) -> None:
        if not name:
            raise ValueError("handler name must be non-empty")
        if name in self._handlers:
            raise ValueError(f"handler already registered: {name}")
        self._handlers[name] = handler

    def register_condition(self, name: str, condition: ConditionHandler) -> None:
        if not name:
            raise ValueError("condition name must be non-empty")
        if name in self._conditions:
            raise ValueError(f"condition already registered: {name}")
        self._conditions[name] = condition

    def validate(self, workflow: WorkflowDefinition) -> None:
        names = [step.name for step in workflow.steps]
        duplicated = sorted({name for name in names if names.count(name) > 1})
        if duplicated:
            raise WorkflowValidationError(f"duplicate step names: {duplicated}")

        name_set = set(names)
        for step in workflow.steps:
            if step.handler not in self._handlers:
                raise WorkflowValidationError(f"missing handler for step {step.name}: {step.handler}")
            if step.condition and step.condition not in self._conditions:
                raise WorkflowValidationError(f"missing condition for step {step.name}: {step.condition}")
            unknown_deps = sorted(set(step.depends_on) - name_set)
            if unknown_deps:
                raise WorkflowValidationError(f"unknown dependencies for step {step.name}: {unknown_deps}")
            if step.name in step.depends_on:
                raise WorkflowValidationError(f"step cannot depend on itself: {step.name}")

        self._topological_order(workflow)

    def run(
        self,
        workflow: WorkflowDefinition,
        input_payload: Optional[Mapping[str, Any]] = None,
        approvals: Optional[Iterable[str]] = None,
        run_id: Optional[str] = None,
    ) -> WorkflowRun:
        self.validate(workflow)
        run_id = run_id or str(uuid.uuid4())
        state = WorkflowState(
            run_id=run_id,
            input=dict(input_payload or {}),
            approvals=set(approvals or []),
            status="running",
        )
        trace: List[TraceEvent] = []
        step_results: Dict[str, StepResult] = {}

        def emit(step: Optional[str], event: str, **payload: Any) -> None:
            trace.append(
                TraceEvent(
                    run_id=run_id,
                    workflow=workflow.name,
                    step=step,
                    event=event,
                    timestamp=time.time(),
                    payload=dict(payload),
                )
            )

        emit(None, "workflow.started", version=workflow.version)
        order = self._topological_order(workflow)
        step_by_name = {step.name: step for step in workflow.steps}

        for step_name in order:
            step = step_by_name[step_name]

            failed_dependencies = [
                dep
                for dep in step.depends_on
                if step_results[dep].status not in {"completed", "skipped"}
            ]
            if failed_dependencies:
                result = StepResult(
                    name=step.name,
                    status="skipped",
                    attempts=0,
                    error=f"blocked by dependencies: {failed_dependencies}",
                )
                step_results[step.name] = result
                emit(step.name, "step.skipped", reason="dependency_failed", dependencies=failed_dependencies)
                continue

            if step.condition:
                condition_result = self._conditions[step.condition](state)
                emit(step.name, "condition.evaluated", condition=step.condition, result=condition_result)
                if not condition_result:
                    result = StepResult(name=step.name, status="skipped", attempts=0)
                    step_results[step.name] = result
                    emit(step.name, "step.skipped", reason="condition_false")
                    continue

            if step.sensitive and step.name not in state.approvals:
                result = StepResult(
                    name=step.name,
                    status="blocked",
                    attempts=0,
                    error="human approval required",
                )
                step_results[step.name] = result
                emit(step.name, "step.blocked", reason="approval_required")
                continue

            result = self._execute_step(workflow.name, step, state, emit)
            step_results[step.name] = result

        if any(result.status == "failed" for result in step_results.values()):
            state.status = "failed"
        elif any(result.status == "blocked" for result in step_results.values()):
            state.status = "blocked"
        else:
            state.status = "completed"

        emit(None, "workflow.finished", status=state.status)
        return WorkflowRun(
            run_id=run_id,
            workflow=workflow.name,
            status=state.status,
            step_results=step_results,
            state=state,
            trace=trace,
        )

    def _execute_step(
        self,
        workflow_name: str,
        step: WorkflowStep,
        state: WorkflowState,
        emit: Callable[..., None],
    ) -> StepResult:
        handler = self._handlers[step.handler]
        max_attempts = step.max_retries + 1
        last_error: Optional[str] = None

        for attempt in range(1, max_attempts + 1):
            emit(step.name, "step.started", attempt=attempt, handler=step.handler)
            try:
                context = WorkflowContext(
                    workflow_name=workflow_name,
                    step_name=step.name,
                    attempt=attempt,
                    state=state,
                )
                output = handler(context)
                state.set(step.name, output)
                emit(step.name, "step.completed", attempt=attempt)
                return StepResult(
                    name=step.name,
                    status="completed",
                    attempts=attempt,
                    output=output,
                )
            except Exception as exc:  # intentionally broad for workflow boundary
                last_error = f"{type(exc).__name__}: {exc}"
                emit(step.name, "step.failed", attempt=attempt, error=last_error)
                if attempt < max_attempts:
                    emit(step.name, "step.retry_scheduled", next_attempt=attempt + 1)

        return StepResult(
            name=step.name,
            status="failed",
            attempts=max_attempts,
            error=last_error,
        )

    def _topological_order(self, workflow: WorkflowDefinition) -> List[str]:
        dependencies = {step.name: set(step.depends_on) for step in workflow.steps}
        ordered: List[str] = []
        ready = sorted([name for name, deps in dependencies.items() if not deps])

        while ready:
            current = ready.pop(0)
            ordered.append(current)
            for name in sorted(dependencies):
                deps = dependencies[name]
                if current in deps:
                    deps.remove(current)
                    if not deps and name not in ordered and name not in ready:
                        ready.append(name)
            ready.sort()

        if len(ordered) != len(workflow.steps):
            remaining = {name: sorted(deps) for name, deps in dependencies.items() if deps}
            raise WorkflowValidationError(f"cycle detected in workflow graph: {remaining}")

        return ordered

    def manifest(self, workflow: WorkflowDefinition) -> JsonDict:
        """Produit un manifeste JSON utile pour la documentation et les agents."""

        self.validate(workflow)
        return {
            "name": workflow.name,
            "version": workflow.version,
            "description": workflow.description,
            "steps": [
                {
                    "name": step.name,
                    "handler": step.handler,
                    "depends_on": list(step.depends_on),
                    "max_retries": step.max_retries,
                    "sensitive": step.sensitive,
                    "condition": step.condition,
                    "timeout_seconds": step.timeout_seconds,
                }
                for step in workflow.steps
            ],
            "execution_order": self._topological_order(workflow),
        }
