import pytest

from rollout_solution import RolloutFailed, rollout


def test_success_promotes_candidate():
    deployed = []
    result = rollout("release-001", "release-002", deployed.append, lambda: True, lambda: True)
    assert deployed == ["release-002"]
    assert result.active_release == "release-002" and result.rolled_back is False


def test_failed_smoke_restores_previous_and_rechecks():
    deployed = []
    checks = iter([False, True])
    result = rollout("release-001", "release-002", deployed.append, lambda: True, lambda: next(checks))
    assert deployed == ["release-002", "release-001"]
    assert result.active_release == "release-001" and result.rolled_back is True


def test_failed_readiness_restores_previous():
    deployed = []
    checks = iter([False, True])
    result = rollout("release-001", "release-002", deployed.append, lambda: next(checks), lambda: True)
    assert result.rolled_back is True


def test_incompatible_schema_is_rejected_before_deploy():
    deployed = []
    with pytest.raises(ValueError, match="Schema"):
        rollout("release-001", "release-002", deployed.append, lambda: True, lambda: True, False)
    assert deployed == []


def test_failure_of_rollback_is_explicit():
    with pytest.raises(RolloutFailed, match="manual recovery"):
        rollout("release-001", "release-002", lambda image: None, lambda: False, lambda: True)


def test_deploy_exception_triggers_recovery():
    calls = []
    def deploy(release):
        calls.append(release)
        if release == "release-002":
            raise TimeoutError
    result = rollout("release-001", "release-002", deploy, lambda: True, lambda: True)
    assert calls == ["release-002", "release-001"] and result.rolled_back
