"""Observability layer for the educational AI agent mini-framework.

The implementation is intentionally dependency-free. It models the core
observability concepts that an AI Engineering team needs before connecting to a
real tracing backend: traces, spans, events, metrics, redaction and JSON export.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Any, Callable, Dict, Iterable, List, Optional
from uuid import uuid4
import json
import re


SENSITIVE_KEYWORDS = (
    "password",
    "secret",
    "token",
    "api_key",
    "apikey",
    "authorization",
    "email",
    "phone",
)


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:16]}"


@dataclass
class ObservabilityConfig:
    """Configuration for the observability layer."""

    service_name: str = "mini_framework"
    include_sensitive_data: bool = False
    redacted_value: str = "[REDACTED]"


@dataclass
class EventRecord:
    """Point-in-time event attached to a trace or span."""

    trace_id: str
    name: str
    message: str
    level: str = "info"
    timestamp: float = field(default_factory=time)
    span_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "name": self.name,
            "message": self.message,
            "level": self.level,
            "timestamp": self.timestamp,
            "attributes": self.attributes,
        }


@dataclass
class MetricPoint:
    """Numeric point used for dashboards and alerts."""

    name: str
    value: float
    unit: str = "count"
    timestamp: float = field(default_factory=time)
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp,
            "attributes": self.attributes,
        }


@dataclass
class SpanRecord:
    """A measured operation inside a trace."""

    trace_id: str
    name: str
    kind: str = "internal"
    span_id: str = field(default_factory=lambda: _new_id("span"))
    parent_id: Optional[str] = None
    start_time: float = field(default_factory=time)
    end_time: Optional[float] = None
    status: str = "running"
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[EventRecord] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def duration_ms(self) -> Optional[float]:
        if self.end_time is None:
            return None
        return round((self.end_time - self.start_time) * 1000, 3)

    def finish(self, status: str = "completed", error: Optional[str] = None) -> None:
        self.status = status
        self.error = error
        self.end_time = time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "kind": self.kind,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms,
            "status": self.status,
            "attributes": self.attributes,
            "error": self.error,
            "events": [event.to_dict() for event in self.events],
        }


@dataclass
class TraceRecord:
    """Logical workflow or agent run."""

    name: str
    trace_id: str = field(default_factory=lambda: _new_id("trace"))
    start_time: float = field(default_factory=time)
    end_time: Optional[float] = None
    status: str = "running"
    attributes: Dict[str, Any] = field(default_factory=dict)
    spans: List[SpanRecord] = field(default_factory=list)
    events: List[EventRecord] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def duration_ms(self) -> Optional[float]:
        if self.end_time is None:
            return None
        return round((self.end_time - self.start_time) * 1000, 3)

    def finish(self, status: str = "completed", error: Optional[str] = None) -> None:
        self.status = status
        self.error = error
        self.end_time = time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms,
            "status": self.status,
            "attributes": self.attributes,
            "error": self.error,
        }


class Observability:
    """Dependency-free tracing, events and metrics collector."""

    def __init__(self, config: Optional[ObservabilityConfig] = None):
        self.config = config or ObservabilityConfig()
        self.traces: Dict[str, TraceRecord] = {}
        self.events: List[EventRecord] = []
        self.metrics: List[MetricPoint] = []
        self._active_trace_stack: List[str] = []
        self._active_span_stack: List[str] = []

    @property
    def current_trace(self) -> Optional[TraceRecord]:
        if not self._active_trace_stack:
            return None
        return self.traces[self._active_trace_stack[-1]]

    @property
    def current_span(self) -> Optional[SpanRecord]:
        trace = self.current_trace
        if trace is None or not self._active_span_stack:
            return None
        current_id = self._active_span_stack[-1]
        for span in reversed(trace.spans):
            if span.span_id == current_id:
                return span
        return None

    def redact(self, value: Any) -> Any:
        """Redact sensitive fields recursively unless explicitly disabled."""

        if self.config.include_sensitive_data:
            return value

        if isinstance(value, dict):
            redacted: Dict[str, Any] = {}
            for key, item in value.items():
                key_lower = str(key).lower()
                if any(word in key_lower for word in SENSITIVE_KEYWORDS):
                    redacted[key] = self.config.redacted_value
                else:
                    redacted[key] = self.redact(item)
            return redacted
        if isinstance(value, list):
            return [self.redact(item) for item in value]
        if isinstance(value, tuple):
            return tuple(self.redact(item) for item in value)
        return value

    def start_trace(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        trace = TraceRecord(name=name, attributes=self.redact(attributes or {}))
        self.traces[trace.trace_id] = trace
        return _TraceContext(self, trace.trace_id)

    def start_span(
        self,
        name: str,
        kind: str = "internal",
        attributes: Optional[Dict[str, Any]] = None,
    ):
        trace = self.current_trace
        if trace is None:
            raise RuntimeError("start_span requires an active trace")
        parent_id = self._active_span_stack[-1] if self._active_span_stack else None
        span = SpanRecord(
            trace_id=trace.trace_id,
            name=name,
            kind=kind,
            parent_id=parent_id,
            attributes=self.redact(attributes or {}),
        )
        trace.spans.append(span)
        return _SpanContext(self, span.span_id)

    def record_event(
        self,
        name: str,
        message: str,
        level: str = "info",
        attributes: Optional[Dict[str, Any]] = None,
    ) -> EventRecord:
        trace = self.current_trace
        if trace is None:
            raise RuntimeError("record_event requires an active trace")
        span = self.current_span
        event = EventRecord(
            trace_id=trace.trace_id,
            span_id=span.span_id if span else None,
            name=name,
            message=message,
            level=level,
            attributes=self.redact(attributes or {}),
        )
        self.events.append(event)
        trace.events.append(event)
        if span:
            span.events.append(event)
        return event

    def record_metric(
        self,
        name: str,
        value: float,
        unit: str = "count",
        attributes: Optional[Dict[str, Any]] = None,
    ) -> MetricPoint:
        trace = self.current_trace
        span = self.current_span
        metric = MetricPoint(
            trace_id=trace.trace_id if trace else None,
            span_id=span.span_id if span else None,
            name=name,
            value=float(value),
            unit=unit,
            attributes=self.redact(attributes or {}),
        )
        self.metrics.append(metric)
        return metric

    def capture_exception(self, exc: BaseException, attributes: Optional[Dict[str, Any]] = None) -> EventRecord:
        current = self.current_span
        if current is not None:
            current.status = "failed"
            current.error = f"{exc.__class__.__name__}: {exc}"
        return self.record_event(
            "exception",
            f"{exc.__class__.__name__}: {exc}",
            level="error",
            attributes=attributes or {},
        )

    def spans(self, trace_id: Optional[str] = None) -> List[SpanRecord]:
        if trace_id is not None:
            return list(self.traces[trace_id].spans)
        all_spans: List[SpanRecord] = []
        for trace in self.traces.values():
            all_spans.extend(trace.spans)
        return all_spans

    def find_spans(
        self,
        *,
        kind: Optional[str] = None,
        status: Optional[str] = None,
        name_contains: Optional[str] = None,
    ) -> List[SpanRecord]:
        result = self.spans()
        if kind is not None:
            result = [span for span in result if span.kind == kind]
        if status is not None:
            result = [span for span in result if span.status == status]
        if name_contains is not None:
            result = [span for span in result if name_contains in span.name]
        return result

    def latency_summary(self) -> Dict[str, Any]:
        durations = [span.duration_ms for span in self.spans() if span.duration_ms is not None]
        by_kind: Dict[str, List[float]] = {}
        for span in self.spans():
            if span.duration_ms is not None:
                by_kind.setdefault(span.kind, []).append(span.duration_ms)

        return {
            "span_count": len(durations),
            "avg_duration_ms": round(sum(durations) / len(durations), 3) if durations else 0.0,
            "max_duration_ms": max(durations) if durations else 0.0,
            "by_kind": {
                kind: {
                    "count": len(values),
                    "avg_duration_ms": round(sum(values) / len(values), 3),
                    "max_duration_ms": max(values),
                }
                for kind, values in by_kind.items()
            },
        }

    def trace_tree(self, trace_id: str) -> List[Dict[str, Any]]:
        trace = self.traces[trace_id]
        children: Dict[Optional[str], List[SpanRecord]] = {}
        for span in trace.spans:
            children.setdefault(span.parent_id, []).append(span)

        def build(span: SpanRecord) -> Dict[str, Any]:
            return {
                "span_id": span.span_id,
                "name": span.name,
                "kind": span.kind,
                "status": span.status,
                "children": [build(child) for child in children.get(span.span_id, [])],
            }

        return [build(root) for root in children.get(None, [])]

    def health_report(self, trace_id: str) -> Dict[str, Any]:
        trace = self.traces[trace_id]
        failed_spans = [span for span in trace.spans if span.status == "failed"]
        error_events = [event for event in trace.events if event.level == "error"]
        return {
            "trace_id": trace_id,
            "trace_name": trace.name,
            "trace_status": trace.status,
            "span_count": len(trace.spans),
            "failed_span_count": len(failed_spans),
            "failed_spans": [
                {"name": span.name, "kind": span.kind, "error": span.error}
                for span in failed_spans
            ],
            "error_event_count": len(error_events),
            "duration_ms": trace.duration_ms,
        }

    def export_json(self) -> Dict[str, Any]:
        return {
            "service_name": self.config.service_name,
            "traces": [trace.to_dict() for trace in self.traces.values()],
            "spans": [span.to_dict() for span in self.spans()],
            "events": [event.to_dict() for event in self.events],
            "metrics": [metric.to_dict() for metric in self.metrics],
            "latency_summary": self.latency_summary(),
        }

    def dumps(self) -> str:
        return json.dumps(self.export_json(), indent=2, sort_keys=True)


class _TraceContext:
    def __init__(self, obs: Observability, trace_id: str):
        self.obs = obs
        self.trace_id = trace_id

    def __enter__(self) -> TraceRecord:
        self.obs._active_trace_stack.append(self.trace_id)
        return self.obs.traces[self.trace_id]

    def __exit__(self, exc_type, exc, tb) -> bool:
        trace = self.obs.traces[self.trace_id]
        status = "failed" if exc else "completed"
        error = f"{exc_type.__name__}: {exc}" if exc else None
        if exc:
            # Event recording still needs the trace on stack.
            self.obs.record_event("exception", error or "Exception", level="error")
        trace.finish(status=status, error=error)
        self.obs._active_trace_stack.pop()
        return False


class _SpanContext:
    def __init__(self, obs: Observability, span_id: str):
        self.obs = obs
        self.span_id = span_id

    def __enter__(self) -> SpanRecord:
        self.obs._active_span_stack.append(self.span_id)
        return self.obs.current_span  # type: ignore[return-value]

    def __exit__(self, exc_type, exc, tb) -> bool:
        span = self.obs.current_span
        if span is None:
            return False
        if exc:
            span.finish(status="failed", error=f"{exc_type.__name__}: {exc}")
            self.obs.record_event("exception", span.error or "Exception", level="error")
        elif span.status == "failed":
            # capture_exception may already have marked the span failed.
            span.finish(status="failed", error=span.error)
        else:
            span.finish(status="completed")
        self.obs._active_span_stack.pop()
        return False


def summarize_export(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Small helper used by the lab and exercises."""

    spans = payload.get("spans", [])
    durations = [
        span["duration_ms"]
        for span in spans
        if isinstance(span.get("duration_ms"), (int, float))
    ]
    failed_spans = [span for span in spans if span.get("status") == "failed"]
    error_events = [event for event in payload.get("events", []) if event.get("level") == "error"]
    return {
        "trace_count": len(payload.get("traces", [])),
        "failed_span_count": len(failed_spans),
        "error_event_count": len(error_events),
        "avg_duration_ms": round(sum(durations) / len(durations), 3) if durations else 0.0,
    }
