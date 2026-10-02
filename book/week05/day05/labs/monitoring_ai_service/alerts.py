from dataclasses import dataclass


@dataclass(frozen=True)
class Alert:
    name: str
    severity: str
    message: str
    runbook: str


@dataclass(frozen=True)
class AlertThresholds:
    max_error_rate: float = 0.05
    max_p95_latency_ms: float = 3000.0
    max_estimated_cost_usd: float = 75.0
    max_empty_responses: int = 10


def evaluate_alerts(
    snapshot: dict,
    thresholds: AlertThresholds = AlertThresholds(),
) -> list[Alert]:
    alerts: list[Alert] = []

    if snapshot.get("error_rate", 0.0) > thresholds.max_error_rate:
        alerts.append(
            Alert(
                name="high_error_rate",
                severity="critical",
                message="Le taux d'erreur dépasse le seuil critique.",
                runbook="check_recent_deployments_and_provider_status",
            )
        )

    if snapshot.get("p95_latency_ms", 0.0) > thresholds.max_p95_latency_ms:
        alerts.append(
            Alert(
                name="high_p95_latency",
                severity="warning",
                message="La latence P95 dépasse l'objectif de production.",
                runbook="inspect_prompt_size_dependencies_and_model_latency",
            )
        )

    if snapshot.get("estimated_cost_usd", 0.0) > thresholds.max_estimated_cost_usd:
        alerts.append(
            Alert(
                name="high_estimated_cost",
                severity="warning",
                message="Le coût estimé dépasse le budget opérationnel.",
                runbook="inspect_token_usage_cache_and_retries",
            )
        )

    if snapshot.get("empty_response_count", 0) > thresholds.max_empty_responses:
        alerts.append(
            Alert(
                name="empty_response_spike",
                severity="warning",
                message="Le nombre de réponses vides dépasse le seuil attendu.",
                runbook="inspect_model_outputs_prompt_changes_and_safety_filters",
            )
        )

    return alerts
