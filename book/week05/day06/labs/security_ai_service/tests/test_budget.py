from concurrent.futures import ThreadPoolExecutor

import pytest

from budget_solution import BudgetDenied, BudgetLedger
from security_ai_service.auth import Principal


def principal(tenant="alpha"):
    return Principal("alice", tenant, frozenset({"chat:write"}))


def test_settlement_releases_unused_units():
    ledger = BudgetLedger()
    reservation = ledger.reserve(principal(), 400)
    assert ledger.snapshot(principal())["available"] == 600
    ledger.settle(reservation, 150)
    assert ledger.snapshot(principal()) == {"consumed": 150, "reserved": 0, "available": 850}


def test_double_settlement_and_double_cancellation_fail():
    ledger = BudgetLedger()
    reservation = ledger.reserve(principal(), 100)
    ledger.settle(reservation, 80)
    with pytest.raises(KeyError):
        ledger.settle(reservation, 80)
    another = ledger.reserve(principal(), 100)
    ledger.cancel(another)
    with pytest.raises(KeyError):
        ledger.cancel(another)
    assert ledger.snapshot(principal())["available"] == 920


def test_tenants_have_independent_accounts():
    ledger = BudgetLedger()
    ledger.reserve(principal(), 1000)
    ledger.reserve(principal("beta"), 1000)
    with pytest.raises(BudgetDenied):
        ledger.reserve(principal(), 1)


def test_concurrent_reservations_do_not_exceed_limit():
    ledger = BudgetLedger()
    def attempt(_):
        try:
            ledger.reserve(principal(), 100)
            return 1
        except BudgetDenied:
            return 0
    with ThreadPoolExecutor(max_workers=8) as pool:
        assert sum(pool.map(attempt, range(50))) == 10
    assert ledger.snapshot(principal())["reserved"] == 1000


def test_actual_usage_over_reservation_keeps_account_locked():
    ledger = BudgetLedger()
    reservation = ledger.reserve(principal(), 100)
    with pytest.raises(ValueError):
        ledger.settle(reservation, 101)
    assert ledger.snapshot(principal())["reserved"] == 100


@pytest.mark.parametrize("value", [-1, 0, True, 1.5])
def test_invalid_reservation_sizes(value):
    with pytest.raises(ValueError):
        BudgetLedger().reserve(principal(), value)
