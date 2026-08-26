# Correction — Challenge

## Implémentation indicative

```python
from mini_framework.workflow import WorkflowDefinition, WorkflowStep, WorkflowEngine

workflow = WorkflowDefinition(
    name="ai_incident_diagnostic",
    version="1.0.0",
    steps=[
        WorkflowStep(name="classify_severity", handler="classify_severity"),
        WorkflowStep(name="collect_context", handler="collect_context", depends_on=("classify_severity",)),
        WorkflowStep(name="hypothesize_root_cause", handler="hypothesize_root_cause", depends_on=("collect_context",)),
        WorkflowStep(
            name="rollback",
            handler="rollback",
            depends_on=("hypothesize_root_cause",),
            condition="should_rollback",
            sensitive=True,
        ),
        WorkflowStep(
            name="final_summary",
            handler="final_summary",
            depends_on=("hypothesize_root_cause", "rollback"),
        ),
    ],
)
```

## Handlers indicatifs

```python
def classify_severity(ctx):
    if ctx.input["error_rate"] > 0.10 or ctx.input["latency_p95_ms"] > 4000:
        return {"severity": "critical"}
    return {"severity": "warning"}

def collect_context(ctx):
    return {
        "service": ctx.input["service"],
        "recent_deploy": ctx.input["recent_deploy"],
        "severity": ctx.data["classify_severity"]["severity"],
    }

def hypothesize_root_cause(ctx):
    if ctx.input["recent_deploy"]:
        cause = "recent deployment regression"
    else:
        cause = "runtime degradation"
    return {"cause": cause}

def rollback(ctx):
    return {"rollback_triggered": True, "service": ctx.input["service"]}

def final_summary(ctx):
    rollback_result = ctx.data.get("rollback")
    return {
        "severity": ctx.data["classify_severity"]["severity"],
        "cause": ctx.data["hypothesize_root_cause"]["cause"],
        "rollback": bool(rollback_result),
    }

def should_rollback(state):
    return (
        state.input.get("recent_deploy") is True
        and state.data["classify_severity"]["severity"] == "critical"
    )
```

## Tests attendus

1. alerte critique sans approbation : `rollback` est `blocked` ;
2. alerte critique avec approbation : `rollback` est `completed` ;
3. alerte non critique : `rollback` est `skipped` ;
4. trace finale contient `workflow.finished` ;
5. la synthèse finale reflète le cas exécuté.

## Point d'attention

Si `final_summary` dépend strictement de `rollback`, elle sera `skipped` lorsque `rollback` est `blocked`. Pour produire une synthèse même en cas de blocage, on peut créer une étape alternative `blocked_summary` ou ajuster le graphe. Dans le lab principal, le choix est conservateur : une action sensible bloquée bloque la suite dépendante.
