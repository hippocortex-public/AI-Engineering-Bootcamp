"""
Shared State Store pédagogique pour un système multi-agent.

Ce module illustre plusieurs principes d'AI Engineering :

- état partagé explicite ;
- versioning ;
- compare-and-set ;
- permissions simples ;
- patch atomique ;
- handoff minimal ;
- event log.

Il n'utilise que la Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Mapping, Optional


Visibility = str


class StateError(Exception):
    """Erreur de base du store d'état."""


class PermissionDenied(StateError):
    """Levée quand un agent tente de lire une clé non autorisée."""


class ConflictError(StateError):
    """Levée quand une écriture versionnée est obsolète."""


class MissingKeyError(StateError):
    """Levée quand une clé demandée n'existe pas."""


@dataclass(frozen=True)
class StateEntry:
    """Entrée versionnée du shared state."""

    key: str
    value: Any
    version: int
    owner: str
    visibility: Visibility
    updated_by: str

    def public_view(self) -> Dict[str, Any]:
        """Retourne une vue sérialisable et stable de l'entrée."""
        return asdict(self)


@dataclass(frozen=True)
class StateEvent:
    """Événement déterministe produit par le store."""

    event_id: int
    agent: str
    operation: str
    key: str
    version: Optional[int]
    status: str
    reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SharedStateStore:
    """
    Store d'état partagé pour un workflow multi-agent.

    Règles :
    - private : visible uniquement par le propriétaire ;
    - shared : visible par tous les agents du workflow ;
    - public : visible par tous les agents du workflow et exportable ;
    - chaque écriture incrémente la version ;
    - expected_version active un contrôle compare-and-set.
    """

    ALLOWED_VISIBILITIES = {"private", "shared", "public"}

    def __init__(self) -> None:
        self._entries: Dict[str, StateEntry] = {}
        self._events: List[StateEvent] = []
        self._next_event_id = 1

    def write(
        self,
        *,
        agent: str,
        key: str,
        value: Any,
        visibility: Visibility = "shared",
        owner: Optional[str] = None,
        expected_version: Optional[int] = None,
    ) -> StateEntry:
        """Écrit une clé versionnée dans le store."""
        self._validate_visibility(visibility)

        current = self._entries.get(key)
        if expected_version is not None:
            current_version = current.version if current else 0
            if current_version != expected_version:
                self._record(
                    agent=agent,
                    operation="write",
                    key=key,
                    version=current_version,
                    status="conflict",
                    reason=f"expected_version={expected_version}",
                )
                raise ConflictError(
                    f"Conflict on {key}: expected version {expected_version}, "
                    f"current version {current_version}"
                )

        next_version = 1 if current is None else current.version + 1
        entry = StateEntry(
            key=key,
            value=value,
            version=next_version,
            owner=owner or (current.owner if current else agent),
            visibility=visibility,
            updated_by=agent,
        )
        self._entries[key] = entry
        self._record(
            agent=agent,
            operation="write",
            key=key,
            version=next_version,
            status="applied",
        )
        return entry

    def read(self, *, agent: str, key: str) -> StateEntry:
        """Lit une entrée si l'agent y a accès."""
        if key not in self._entries:
            self._record(
                agent=agent,
                operation="read",
                key=key,
                version=None,
                status="missing",
                reason="key_not_found",
            )
            raise MissingKeyError(key)

        entry = self._entries[key]
        if not self._can_read(agent, entry):
            self._record(
                agent=agent,
                operation="read",
                key=key,
                version=entry.version,
                status="denied",
                reason="private_entry",
            )
            raise PermissionDenied(f"{agent} cannot read {key}")

        self._record(
            agent=agent,
            operation="read",
            key=key,
            version=entry.version,
            status="allowed",
        )
        return entry

    def delete(
        self,
        *,
        agent: str,
        key: str,
        expected_version: Optional[int] = None,
    ) -> None:
        """Supprime une clé avec contrôle de version optionnel."""
        if key not in self._entries:
            self._record(
                agent=agent,
                operation="delete",
                key=key,
                version=None,
                status="missing",
                reason="key_not_found",
            )
            raise MissingKeyError(key)

        current = self._entries[key]
        if expected_version is not None and current.version != expected_version:
            self._record(
                agent=agent,
                operation="delete",
                key=key,
                version=current.version,
                status="conflict",
                reason=f"expected_version={expected_version}",
            )
            raise ConflictError(
                f"Conflict on delete {key}: expected version {expected_version}, "
                f"current version {current.version}"
            )

        del self._entries[key]
        self._record(
            agent=agent,
            operation="delete",
            key=key,
            version=current.version,
            status="applied",
        )

    def apply_patch(
        self,
        *,
        agent: str,
        writes: Mapping[str, Mapping[str, Any]],
    ) -> Dict[str, StateEntry]:
        """
        Applique un patch multi-clés atomiquement.

        Format d'une écriture :

        {
            "value": ...,
            "visibility": "shared",
            "owner": "triage",
            "expected_version": 1
        }

        La méthode valide d'abord tout le patch, puis applique les changements.
        """
        prepared: Dict[str, StateEntry] = {}

        for key, spec in writes.items():
            visibility = str(spec.get("visibility", "shared"))
            self._validate_visibility(visibility)

            current = self._entries.get(key)
            expected = spec.get("expected_version")
            if expected is not None:
                current_version = current.version if current else 0
                if current_version != expected:
                    self._record(
                        agent=agent,
                        operation="patch",
                        key=key,
                        version=current_version,
                        status="conflict",
                        reason=f"expected_version={expected}",
                    )
                    raise ConflictError(
                        f"Patch conflict on {key}: expected version {expected}, "
                        f"current version {current_version}"
                    )

            next_version = 1 if current is None else current.version + 1
            prepared[key] = StateEntry(
                key=key,
                value=spec.get("value"),
                version=next_version,
                owner=str(spec.get("owner") or (current.owner if current else agent)),
                visibility=visibility,
                updated_by=agent,
            )

        for key, entry in prepared.items():
            self._entries[key] = entry
            self._record(
                agent=agent,
                operation="patch",
                key=key,
                version=entry.version,
                status="applied",
            )

        return prepared

    def snapshot(self, *, agent: str) -> Dict[str, Dict[str, Any]]:
        """Retourne les clés visibles par un agent."""
        return {
            key: entry.public_view()
            for key, entry in sorted(self._entries.items())
            if self._can_read(agent, entry)
        }

    def create_handoff(
        self,
        *,
        from_agent: str,
        to_agent: str,
        keys: Iterable[str],
    ) -> Dict[str, Any]:
        """
        Produit un contexte minimal de handoff.

        Les clés privées non autorisées sont ignorées pour éviter les fuites.
        """
        context: Dict[str, Dict[str, Any]] = {}
        for key in keys:
            entry = self._entries.get(key)
            if entry is None:
                continue
            if not self._can_read(to_agent, entry):
                continue
            context[key] = {
                "value": entry.value,
                "version": entry.version,
                "visibility": entry.visibility,
                "owner": entry.owner,
            }

        self._record(
            agent=from_agent,
            operation="handoff",
            key=f"{from_agent}->{to_agent}",
            version=None,
            status="created",
        )
        return {"from": from_agent, "to": to_agent, "context": context}

    def export_as_mcp_resource(
        self,
        *,
        uri: str,
        agent: str,
        include_shared: bool = True,
    ) -> Dict[str, Any]:
        """
        Exporte une vue filtrée comme ressource MCP pédagogique.

        Par défaut, les clés `public` et `shared` visibles par l'agent sont incluses.
        Les clés `private` ne sont jamais exportées sauf si elles appartiennent
        à l'agent et que l'appelant modifie explicitement cette méthode.
        """
        exported: Dict[str, Dict[str, Any]] = {}
        for key, entry in sorted(self._entries.items()):
            if entry.visibility == "public":
                exported[key] = entry.public_view()
            elif include_shared and entry.visibility == "shared" and self._can_read(agent, entry):
                exported[key] = entry.public_view()

        text = {
            "uri": uri,
            "state": exported,
            "event_count": len(self._events),
        }
        return {
            "uri": uri,
            "mimeType": "application/json",
            "text": text,
        }

    def events(self) -> List[Dict[str, Any]]:
        """Retourne le journal d'événements."""
        return [event.to_dict() for event in self._events]

    def summary(self) -> Dict[str, Any]:
        """Produit un résumé déterministe du store."""
        return {
            "keys": sorted(self._entries.keys()),
            "versions": {
                key: entry.version
                for key, entry in sorted(self._entries.items())
            },
            "event_count": len(self._events),
        }

    def _validate_visibility(self, visibility: str) -> None:
        if visibility not in self.ALLOWED_VISIBILITIES:
            raise ValueError(
                f"visibility must be one of {sorted(self.ALLOWED_VISIBILITIES)}"
            )

    def _can_read(self, agent: str, entry: StateEntry) -> bool:
        if entry.visibility == "private":
            return entry.owner == agent
        return entry.visibility in {"shared", "public"}

    def _record(
        self,
        *,
        agent: str,
        operation: str,
        key: str,
        version: Optional[int],
        status: str,
        reason: Optional[str] = None,
    ) -> None:
        self._events.append(
            StateEvent(
                event_id=self._next_event_id,
                agent=agent,
                operation=operation,
                key=key,
                version=version,
                status=status,
                reason=reason,
            )
        )
        self._next_event_id += 1


class LocalAgentWorkspace:
    """
    Espace local d'un agent.

    Il sert à montrer que l'état local ne doit pas être implicitement partagé.
    """

    def __init__(self, agent: str) -> None:
        self.agent = agent
        self._data: Dict[str, Any] = {}

    def set_private_note(self, key: str, value: Any) -> None:
        self._data[key] = value

    def export_patch(self, *, key: str, visibility: str = "shared") -> Dict[str, Dict[str, Any]]:
        if key not in self._data:
            raise MissingKeyError(key)
        return {
            key: {
                "value": self._data[key],
                "visibility": visibility,
                "owner": self.agent,
            }
        }


def run_demo() -> Dict[str, Any]:
    """Démonstration exécutable du store."""
    store = SharedStateStore()
    store.write(
        agent="coordinator",
        key="objective",
        value="Diagnostiquer incident checkout",
        visibility="public",
    )
    store.write(
        agent="triage",
        key="triage.private_notes",
        value="Hypothèse non vérifiée : cache instable",
        visibility="private",
        owner="triage",
    )
    store.apply_patch(
        agent="triage",
        writes={
            "incident.summary": {
                "value": "Erreur 500 intermittente sur /checkout",
                "visibility": "shared",
                "owner": "triage",
            },
            "incident.status": {
                "value": "investigating",
                "visibility": "public",
                "owner": "coordinator",
            },
        },
    )
    handoff = store.create_handoff(
        from_agent="triage",
        to_agent="backend",
        keys=["objective", "incident.summary", "incident.status", "triage.private_notes"],
    )
    return {
        "summary": store.summary(),
        "backend_snapshot": store.snapshot(agent="backend"),
        "handoff": handoff,
        "events": store.events(),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
