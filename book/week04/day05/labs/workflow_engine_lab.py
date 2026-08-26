"""Lab — Workflow Engine pour le mini-framework d'agents.

Le lab simule un workflow de support IA :
1. classifier une demande ;
2. enrichir le contexte ;
3. proposer un plan ;
4. exécuter une action sensible si elle est approuvée ;
5. produire une synthèse finale.

Le code est déterministe afin d'être testable sans API externe.
"""

from __future__ import annotations

from pathlib import Path
import sys

# Permet d'exécuter le lab depuis son dossier sans installation du package.
ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mini_framework.workflow import WorkflowDefinition, WorkflowEngine, WorkflowStep


def build_support_workflow() -> WorkflowDefinition:
    """Définit le workflow pédagogique principal."""

    return WorkflowDefinition(
        name="support_resolution_workflow",
        version="1.0.0",
        description="Workflow déterministe pour résoudre une demande support avec contrôle humain.",
        steps=[
            WorkflowStep(name="classify", handler="classify_ticket"),
            WorkflowStep(name="enrich", handler="enrich_context", depends_on=("classify",)),
            WorkflowStep(name="plan", handler="draft_resolution_plan", depends_on=("enrich",), max_retries=1),
            WorkflowStep(
                name="refund",
                handler="issue_refund",
                depends_on=("plan",),
                sensitive=True,
                condition="is_refund_required",
            ),
            WorkflowStep(name="final_answer", handler="compose_final_answer", depends_on=("plan", "refund")),
        ],
    )


def register_support_handlers(engine: WorkflowEngine) -> None:
    """Enregistre les handlers et conditions du workflow."""

    def classify_ticket(ctx):
        text = ctx.input.get("message", "").lower()
        if "refund" in text or "remboursement" in text:
            intent = "refund"
        elif "bug" in text or "erreur" in text:
            intent = "bug"
        else:
            intent = "general"
        return {"intent": intent, "priority": "high" if "urgent" in text else "normal"}

    def enrich_context(ctx):
        classification = ctx.data["classify"]
        return {
            "customer_tier": ctx.input.get("customer_tier", "standard"),
            "intent": classification["intent"],
            "known_policy": "refund_allowed_with_human_approval",
        }

    def draft_resolution_plan(ctx):
        if ctx.input.get("force_plan_failure") and ctx.attempt == 1:
            raise RuntimeError("temporary planner failure")
        intent = ctx.data["classify"]["intent"]
        if intent == "refund":
            steps = ["verify order", "request human approval", "issue refund", "notify customer"]
        elif intent == "bug":
            steps = ["collect environment", "open diagnostic", "propose workaround"]
        else:
            steps = ["answer question", "offer escalation if needed"]
        return {"intent": intent, "steps": steps, "requires_refund": intent == "refund"}

    def issue_refund(ctx):
        amount = float(ctx.input.get("amount", 0.0))
        if amount <= 0:
            raise ValueError("amount must be positive")
        return {"refund_id": "rf_demo_001", "amount": amount, "currency": "EUR"}

    def compose_final_answer(ctx):
        plan = ctx.data["plan"]
        refund = ctx.data.get("refund")
        if refund:
            return {
                "status": "resolved",
                "message": f"Refund issued for {refund['amount']} {refund['currency']}.",
                "next_steps": plan["steps"],
            }
        return {
            "status": "resolved",
            "message": "A resolution plan has been prepared.",
            "next_steps": plan["steps"],
        }

    def is_refund_required(state):
        plan = state.data.get("plan", {})
        return bool(plan.get("requires_refund"))

    engine.register_handler("classify_ticket", classify_ticket)
    engine.register_handler("enrich_context", enrich_context)
    engine.register_handler("draft_resolution_plan", draft_resolution_plan)
    engine.register_handler("issue_refund", issue_refund)
    engine.register_handler("compose_final_answer", compose_final_answer)
    engine.register_condition("is_refund_required", is_refund_required)


def run_demo():
    engine = WorkflowEngine()
    register_support_handlers(engine)
    workflow = build_support_workflow()
    return engine.run(
        workflow,
        input_payload={
            "message": "Urgent refund request for a duplicated charge",
            "customer_tier": "premium",
            "amount": 42.0,
        },
        approvals={"refund"},
        run_id="demo_run",
    )


if __name__ == "__main__":
    result = run_demo()
    print(result.to_json())
