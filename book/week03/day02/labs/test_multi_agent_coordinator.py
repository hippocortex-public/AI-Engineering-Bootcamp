"""
Tests du lab Semaine 3 — Jour 2 — Coordination multi-agents.

Exécution :
    python test_multi_agent_coordinator.py
"""

from multi_agent_coordinator import (
    AgentObservation,
    CoordinationPolicy,
    CoordinationTask,
    MultiAgentCoordinator,
    SpecialistAgent,
    build_default_registry,
    detect_conflicts,
)


def test_registry_selects_relevant_agents_only():
    registry = build_default_registry()
    task = CoordinationTask(
        task_id="t1",
        objective="Investigate duplicated invoice",
        domains=["billing"],
        risk_level="low",
    )
    selected = registry.select_by_domains(task.domains)
    assert [agent.name for agent in selected] == ["billing_agent"]


def test_plan_uses_parallel_mode_for_multiple_agents():
    coordinator = MultiAgentCoordinator(build_default_registry())
    task = CoordinationTask(
        task_id="t2",
        objective="Prepare customer response about payment bug",
        domains=["support", "billing", "engineering"],
        risk_level="medium",
    )
    plan = coordinator.build_plan(task)
    assert plan.execution_mode == "parallel"
    assert plan.selected_agents == ["billing_agent", "engineering_agent", "support_agent"]


def test_high_risk_triggers_review():
    coordinator = MultiAgentCoordinator(build_default_registry())
    task = CoordinationTask(
        task_id="t3",
        objective="Analyze possible data exposure",
        domains=["security", "support"],
        risk_level="high",
    )
    result = coordinator.run(task)
    assert result.review_performed is True
    assert "reviewer_agent" in [observation.agent for observation in result.observations]
    assert result.status == "needs_review"


def test_security_domain_triggers_review_even_if_risk_is_medium():
    coordinator = MultiAgentCoordinator(build_default_registry())
    task = CoordinationTask(
        task_id="t4",
        objective="Explain permission issue",
        domains=["security", "support"],
        risk_level="medium",
    )
    result = coordinator.run(task)
    assert result.review_performed is True


def test_unknown_domain_needs_clarification():
    coordinator = MultiAgentCoordinator(build_default_registry())
    task = CoordinationTask(
        task_id="t5",
        objective="Handle unsupported request",
        domains=["unknown"],
        risk_level="low",
    )
    result = coordinator.run(task)
    assert result.selected_agents == []
    assert result.review_performed is True
    assert result.status == "needs_clarification"


def test_conflict_detection_between_resolved_and_unresolved():
    observations = [
        AgentObservation(
            agent="engineering_agent",
            status="resolved",
            finding="Bug fixed.",
            confidence=0.8,
            domains=["engineering"],
        ),
        AgentObservation(
            agent="support_agent",
            status="unresolved",
            finding="Customer still reports the issue.",
            confidence=0.8,
            domains=["support"],
        ),
    ]
    conflicts = detect_conflicts(observations)
    assert len(conflicts) == 1
    assert "conflicts with" in conflicts[0]


def test_conflict_triggers_needs_clarification_with_custom_agent_status():
    registry = build_default_registry()
    registry.register(
        SpecialistAgent(
            name="incident_customer_agent",
            domains=["incident_customer"],
            default_status="unresolved",
            summary_template="Customer signal for {task_id}: issue still present.",
            confidence=0.7,
        )
    )
    coordinator = MultiAgentCoordinator(registry)

    task = CoordinationTask(
        task_id="t6",
        objective="Compare incident status with customer signal",
        domains=["engineering", "incident_customer"],
        risk_level="medium",
    )
    result = coordinator.run(task)
    assert result.conflicts
    assert result.review_performed is True
    assert result.status == "needs_clarification"


def test_context_is_filtered_to_matching_domains():
    registry = build_default_registry()
    billing_agent = registry.get("billing_agent")
    task = CoordinationTask(
        task_id="t7",
        objective="Investigate invoice and API issue",
        domains=["billing", "engineering"],
        risk_level="medium",
    )
    context = billing_agent.build_context(task)
    assert context.domains == ["billing"]


def test_result_is_json_serializable():
    coordinator = MultiAgentCoordinator(build_default_registry())
    task = CoordinationTask(
        task_id="t8",
        objective="Summarize product feedback",
        domains=["product"],
        risk_level="low",
    )
    result = coordinator.run(task)
    encoded = result.to_json()
    assert '"task_id": "t8"' in encoded
    assert '"trace"' in encoded


def test_sensitive_action_triggers_review():
    coordinator = MultiAgentCoordinator(build_default_registry())
    task = CoordinationTask(
        task_id="t9",
        objective="Prepare refund approval response",
        domains=["billing", "support"],
        risk_level="medium",
        sensitive_action=True,
    )
    result = coordinator.run(task)
    assert result.review_performed is True


def test_policy_rejects_invalid_max_rounds():
    try:
        CoordinationPolicy(max_rounds=0)
    except ValueError as exc:
        assert "max_rounds" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def run_all_tests():
    tests = [
        test_registry_selects_relevant_agents_only,
        test_plan_uses_parallel_mode_for_multiple_agents,
        test_high_risk_triggers_review,
        test_security_domain_triggers_review_even_if_risk_is_medium,
        test_unknown_domain_needs_clarification,
        test_conflict_detection_between_resolved_and_unresolved,
        test_conflict_triggers_needs_clarification_with_custom_agent_status,
        test_context_is_filtered_to_matching_domains,
        test_result_is_json_serializable,
        test_sensitive_action_triggers_review,
        test_policy_rejects_invalid_max_rounds,
    ]

    for test in tests:
        test()

    print(f"{len(tests)} tests passed")


if __name__ == "__main__":
    run_all_tests()
