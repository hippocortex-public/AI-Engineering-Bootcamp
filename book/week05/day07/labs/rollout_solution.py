"""Corrigé de décision : callbacks simulés, aucune commande Docker exécutée ici."""
from dataclasses import dataclass


class RolloutFailed(Exception):
    pass


@dataclass(frozen=True)
class RolloutResult:
    active_release: str
    rolled_back: bool


def rollout(previous, candidate, deploy, readiness, smoke, schema_compatible=True):
    if not previous or not candidate or previous == candidate:
        raise ValueError("Distinct previous and candidate releases are required")
    if not schema_compatible:
        raise ValueError("Schema is incompatible with rollback")
    try:
        # Le callback deploy doit contenir son propre délai maximal.
        deploy(candidate)
        if not readiness() or not smoke():
            raise RolloutFailed("Candidate failed release checks")
        return RolloutResult(candidate, False)
    except Exception:
        try:
            deploy(previous)
            if not readiness() or not smoke():
                raise RolloutFailed("Previous release failed recovery checks")
        except Exception:
            raise RolloutFailed("Rollback failed; manual recovery required") from None
        return RolloutResult(previous, True)
