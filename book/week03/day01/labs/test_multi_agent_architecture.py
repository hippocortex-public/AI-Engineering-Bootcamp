from multi_agent_architecture import (
    AgentSpec,
    ArchitectureError,
    MultiAgentArchitecture,
    Task,
    build_default_architecture,
)


def test_routes_billing_ticket():
    architecture = build_default_architecture()
    decision = architecture.route(Task("T1", "I have a payment issue with my invoice."))
    assert decision.target_agent == "billing"
    assert decision.requires_clarification is False
    assert decision.confidence > 0.5


def test_routes_refund_ticket():
    architecture = build_default_architecture()
    decision = architecture.route(Task("T2", "Can I get a refund or money back?"))
    assert decision.target_agent == "refund"


def test_unknown_request_requires_clarification():
    architecture = build_default_architecture()
    decision = architecture.route(Task("T3", "Hello, I need help."))
    assert decision.target_agent is None
    assert decision.requires_clarification is True


def test_ambiguous_request_requires_clarification():
    architecture = build_default_architecture()
    decision = architecture.route(Task("T4", "I have an invoice bug."))
    assert decision.requires_clarification is True


def test_manager_worker_runs_reviewer():
    architecture = build_default_architecture()
    run = architecture.run_manager_worker(Task("T5", "My subscription payment failed."))
    assert run.reviewed is True
    assert run.result is not None
    assert run.result.agent == "reviewer"
    assert "Réponse validée" in run.final_answer
    assert [event.agent for event in run.trace] == ["manager", "router", "billing", "reviewer", "manager"]


def test_handoff_specialist_takes_control_without_reviewer():
    architecture = build_default_architecture()
    run = architecture.run_handoff(Task("T6", "I want to cancel and get a refund."))
    assert run.reviewed is False
    assert run.result is not None
    assert run.result.agent == "refund"
    assert run.trace[-1].action == "take_control"


def test_high_risk_request_requires_human_review():
    architecture = build_default_architecture()
    result = architecture.run_specialist("technical", Task("T7", "There is a legal breach in logs."))
    assert result.risk_level == "high"
    assert result.requires_human_review is True


def test_parallel_review_runs_selected_specialists():
    architecture = build_default_architecture()
    results = architecture.run_parallel_review(
        Task("T8", "Analyze this product and billing request."),
        selected_agents=["billing", "product", "reviewer"],
    )
    assert [result.agent for result in results] == ["billing", "product"]


def test_architecture_requires_reviewer():
    try:
        MultiAgentArchitecture([AgentSpec("billing", "Billing Specialist", ("invoice",))])
    except ArchitectureError as exc:
        assert "reviewer" in str(exc)
    else:
        raise AssertionError("ArchitectureError was expected.")


def test_run_is_json_serializable():
    architecture = build_default_architecture()
    run = architecture.run_manager_worker(Task("T9", "I have a payment problem."))
    payload = run.to_json()
    assert '"ticket_id": "T9"' in payload
    assert '"trace"' in payload


def test_lab_extension_with_security_agent():
    agents = [
        AgentSpec("security", "Security Specialist", ("security", "access", "breach", "permission"), ("get_security_policy",)),
        AgentSpec("billing", "Billing Specialist", ("invoice",)),
        AgentSpec("reviewer", "Reviewer Agent", ()),
    ]
    architecture = MultiAgentArchitecture(agents)
    decision = architecture.route(Task("T10", "I suspect a security breach on my account."))
    assert decision.target_agent == "security"


if __name__ == "__main__":
    tests = [
        test_routes_billing_ticket,
        test_routes_refund_ticket,
        test_unknown_request_requires_clarification,
        test_ambiguous_request_requires_clarification,
        test_manager_worker_runs_reviewer,
        test_handoff_specialist_takes_control_without_reviewer,
        test_high_risk_request_requires_human_review,
        test_parallel_review_runs_selected_specialists,
        test_architecture_requires_reviewer,
        test_run_is_json_serializable,
        test_lab_extension_with_security_agent,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} tests passed")
