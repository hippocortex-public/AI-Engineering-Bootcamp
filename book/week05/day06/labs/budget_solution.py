"""Corrigé pédagogique : budget d'unités estimées, non monétaire, en mémoire."""
from dataclasses import dataclass
from threading import Lock
from uuid import uuid4

from security_ai_service.auth import Principal


class BudgetDenied(Exception):
    pass


@dataclass
class Account:
    consumed: int = 0
    reserved: int = 0


@dataclass(frozen=True)
class Reservation:
    owner: tuple[str, str]
    amount: int


class BudgetLedger:
    def __init__(self, limit: int = 1000) -> None:
        self._validate_units(limit, positive=True)
        self.limit = limit
        self._accounts: dict[tuple[str, str], Account] = {}
        self._reservations: dict[str, Reservation] = {}
        self._lock = Lock()

    @staticmethod
    def _validate_units(value: int, positive: bool = False) -> None:
        if type(value) is not int or value < (1 if positive else 0):
            raise ValueError("Invalid token units")

    def reserve(self, principal: Principal, estimated_tokens: int) -> str:
        self._validate_units(estimated_tokens, positive=True)
        owner = (principal.tenant, principal.subject)
        with self._lock:
            account = self._accounts.setdefault(owner, Account())
            if account.consumed + account.reserved + estimated_tokens > self.limit:
                raise BudgetDenied
            reservation_id = uuid4().hex
            self._reservations[reservation_id] = Reservation(owner, estimated_tokens)
            account.reserved += estimated_tokens
            return reservation_id

    def settle(self, reservation_id: str, actual_tokens: int) -> None:
        self._validate_units(actual_tokens)
        with self._lock:
            reservation = self._reservations[reservation_id]
            if actual_tokens > reservation.amount:
                # Réservation conservée : réconciliation nécessaire.
                raise ValueError("Actual usage exceeds reservation")
            account = self._accounts[reservation.owner]
            account.reserved -= reservation.amount
            account.consumed += actual_tokens
            del self._reservations[reservation_id]

    def cancel(self, reservation_id: str) -> None:
        with self._lock:
            reservation = self._reservations.pop(reservation_id)
            self._accounts[reservation.owner].reserved -= reservation.amount

    def snapshot(self, principal: Principal) -> dict[str, int]:
        with self._lock:
            account = self._accounts.get((principal.tenant, principal.subject), Account())
            return {"consumed": account.consumed, "reserved": account.reserved,
                    "available": self.limit - account.consumed - account.reserved}
