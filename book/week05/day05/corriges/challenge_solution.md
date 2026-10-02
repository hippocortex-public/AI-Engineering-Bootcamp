# Corrigé — Challenge

## Architecture proposée

Le monitoring minimal est séparé en cinq composants :

```text
app.py        API FastAPI et routes
metrics.py    collecte et agrégation des métriques
cost.py       estimation de coût par modèle
alerts.py     règles d’alerte
redaction.py  filtrage des données sensibles
```

Cette séparation permet de tester la logique métier du monitoring sans démarrer un vrai fournisseur LLM.

## Modèle de requête monitorée

```python
from dataclasses import dataclass
from time import time

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
    timestamp: float = time()
```

## Collecteur de métriques

```python
class MetricsStore:
    def __init__(self) -> None:
        self.records = []

    def record(self, record: RequestRecord) -> None:
        self.records.append(record)

    def snapshot(self) -> dict:
        request_count = len(self.records)
        error_count = sum(1 for r in self.records if r.status_code >= 500)
        empty_response_count = sum(1 for r in self.records if r.empty_response)
        total_prompt_tokens = sum(r.prompt_tokens for r in self.records)
        total_completion_tokens = sum(r.completion_tokens for r in self.records)
        estimated_cost_usd = sum(r.estimated_cost_usd for r in self.records)
        latencies = sorted(r.latency_ms for r in self.records)

        if not request_count:
            p95_latency_ms = 0.0
            avg_latency_ms = 0.0
        else:
            avg_latency_ms = sum(latencies) / request_count
            index = max(0, int(0.95 * request_count) - 1)
            p95_latency_ms = latencies[index]

        return {
            "request_count": request_count,
            "error_count": error_count,
            "error_rate": error_count / request_count if request_count else 0.0,
            "empty_response_count": empty_response_count,
            "avg_latency_ms": avg_latency_ms,
            "p95_latency_ms": p95_latency_ms,
            "total_prompt_tokens": total_prompt_tokens,
            "total_completion_tokens": total_completion_tokens,
            "estimated_cost_usd": estimated_cost_usd,
        }
```

## Estimation de coût

```python
def estimate_cost(prompt_tokens, completion_tokens, input_price_per_1k, output_price_per_1k):
    return (
        prompt_tokens / 1000 * input_price_per_1k
        + completion_tokens / 1000 * output_price_per_1k
    )
```

## Règles d’alerte

```python
def evaluate_alerts(snapshot):
    alerts = []

    if snapshot["error_rate"] > 0.05:
        alerts.append("high_error_rate")

    if snapshot["p95_latency_ms"] > 3000:
        alerts.append("high_p95_latency")

    if snapshot["estimated_cost_usd"] > 75:
        alerts.append("high_estimated_cost")

    if snapshot["empty_response_count"] > 10:
        alerts.append("empty_response_spike")

    return alerts
```

## Redaction

```python
import re

def redact_sensitive_text(text: str) -> str:
    text = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[REDACTED_EMAIL]", text)
    text = re.sub(r"sk-[A-Za-z0-9_-]+", "[REDACTED_SECRET]", text)
    return text
```

## Tests attendus

Les tests doivent couvrir au minimum :

- calcul du coût ;
- agrégation du nombre de requêtes ;
- calcul du taux d’erreur ;
- calcul de la latence P95 ;
- détection d’une alerte ;
- redaction d’un email et d’une clé API.

## Explication

Ce design rend le monitoring indépendant du fournisseur LLM. Il peut donc être validé en local, intégré à une API FastAPI, puis remplacé ou enrichi plus tard avec Prometheus, OpenTelemetry ou une plateforme d’observabilité complète.
