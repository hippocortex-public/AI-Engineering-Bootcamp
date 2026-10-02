from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from time import time
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class RequestRecord:
    request_id: str
    route: str
    status_code: int
    latency_ms: float
    prompt_tokens: int
    completion_tokens: int
    estimated_cost_usd: float
    empty_response: bool
    model_name: str = "simulated-model"
    timestamp: float = field(default_factory=time)


class MetricsStore:
    """Collecteur en mémoire pour comprendre les principes de monitoring.

    En production, ce composant serait remplacé ou complété par Prometheus,
    OpenTelemetry, Datadog, Grafana Cloud ou une autre plateforme.
    """

    def __init__(self) -> None:
        self._records: list[RequestRecord] = []
        self._lock = Lock()
        self.started_at = time()

    def new_request_id(self) -> str:
        return f"req_{uuid4().hex[:12]}"

    def record(self, record: RequestRecord) -> None:
        self._validate_record(record)
        with self._lock:
            self._records.append(record)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            records = list(self._records)

        request_count = len(records)
        error_count = sum(1 for r in records if r.status_code >= 500)
        empty_response_count = sum(1 for r in records if r.empty_response)
        total_prompt_tokens = sum(r.prompt_tokens for r in records)
        total_completion_tokens = sum(r.completion_tokens for r in records)
        estimated_cost_usd = round(sum(r.estimated_cost_usd for r in records), 6)
        latencies = [r.latency_ms for r in records]

        return {
            "request_count": request_count,
            "error_count": error_count,
            "error_rate": round(error_count / request_count, 6) if request_count else 0.0,
            "empty_response_count": empty_response_count,
            "avg_latency_ms": round(sum(latencies) / request_count, 3) if request_count else 0.0,
            "p95_latency_ms": round(percentile(latencies, 95), 3) if request_count else 0.0,
            "total_prompt_tokens": total_prompt_tokens,
            "total_completion_tokens": total_completion_tokens,
            "total_tokens": total_prompt_tokens + total_completion_tokens,
            "estimated_cost_usd": estimated_cost_usd,
            "uptime_seconds": round(time() - self.started_at, 3),
        }

    def reset(self) -> None:
        with self._lock:
            self._records.clear()
            self.started_at = time()

    @staticmethod
    def _validate_record(record: RequestRecord) -> None:
        if record.latency_ms < 0:
            raise ValueError("latency_ms must be positive or zero.")
        if record.prompt_tokens < 0 or record.completion_tokens < 0:
            raise ValueError("Token counts must be positive or zero.")
        if record.estimated_cost_usd < 0:
            raise ValueError("estimated_cost_usd must be positive or zero.")


def percentile(values: list[float], percentile_rank: int) -> float:
    """Calcule un percentile simple sans dépendance externe.

    Cette implémentation est volontairement lisible pour un lab pédagogique.
    """

    if not values:
        return 0.0

    if not 0 <= percentile_rank <= 100:
        raise ValueError("percentile_rank must be between 0 and 100.")

    sorted_values = sorted(values)
    if len(sorted_values) == 1:
        return sorted_values[0]

    index = round((percentile_rank / 100) * (len(sorted_values) - 1))
    return sorted_values[index]
