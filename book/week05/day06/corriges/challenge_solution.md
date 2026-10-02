# Corrigé du challenge — Réserver avant de consommer

## Invariant

Sous le verrou, `consumed + reserved` ne dépasse pas le plafond lorsqu'une
réservation est créée. La finalisation retire la totalité réservée puis ajoute la
consommation réelle. Une réservation retirée ne peut plus être finalisée ou annulée.
La clé de compte reste `(tenant, subject)` ; une rotation de clé ne crée pas un compte.

## Implémentation exécutable

Le code ci-dessous correspond à `labs/budget_solution.py`. Les identifiants retournés
restent internes au backend ; ils ne constituent pas une API publique d'autorisation.

```python
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
```

## Démonstration

```python
alice = Principal("alice", "alpha", frozenset({"chat:write"}))
bob = Principal("bob", "beta", frozenset({"chat:write"}))
ledger = BudgetLedger(1000)
r1 = ledger.reserve(alice, 400)
assert ledger.snapshot(alice)["available"] == 600
ledger.settle(r1, 150)
assert ledger.snapshot(alice) == {"consumed": 150, "reserved": 0, "available": 850}
r2 = ledger.reserve(alice, 200)
ledger.cancel(r2)
assert ledger.snapshot(alice)["available"] == 850
assert ledger.snapshot(bob)["available"] == 1000
try:
    ledger.settle(r1, 150)
except KeyError:
    print("Double finalisation refusée")
else:
    raise AssertionError("Double comptage possible")
```

## Tests et limites

Les tests dans `test_budget.py` couvrent les réservations concurrentes, l'isolation,
la libération et le dépassement réel. Cette classe n'est pas branchée automatiquement
sur `/chat` : le challenge consiste aussi à choisir le bon point d'insertion avant
l'appel fournisseur et après la vérification des droits documentaires.

Pour l'intégration : réserver sur une identité fiable, conserver l'identifiant côté
backend, appeler le fournisseur, rapprocher la consommation puis finaliser. Annuler
seulement si l'on sait que l'appel n'a pas consommé ; un timeout peut avoir été facturé.
Si la consommation dépasse la réservation, la classe garde celle-ci. Un processus
de réconciliation doit enregistrer le dépassement et bloquer ou adapter la suite.

La limite de consommation réelle inférieure à la réservation est une hypothèse
du simulateur. Elle ne représente pas une garantie de facturation d'un fournisseur.
Limiter la sortie et tenir compte des mécanismes de cache, retries et reasoning
propres au fournisseur quand ils influencent la consommation.

## Migration Redis

Stocker comptes et réservations dans un domaine de clés cohérent. Exécuter réservation,
finalisation et annulation atomiquement par script. En Redis Cluster, choisir des
hash tags compatibles avec l'opération multi-clés. Conserver une clé d'idempotence
pour rapprocher les retries et des états explicites plutôt que perdre la trace d'une
réservation. Une expiration ne doit pas libérer automatiquement un budget pour un
appel encore actif. Définir une récupération des réservations abandonnées et la
politique de refus lorsque le registre de budget est indisponible. Tester crash,
retry, concurrence et réconciliation ; ne pas promettre une transaction atomique
entre Redis et le fournisseur externe.
