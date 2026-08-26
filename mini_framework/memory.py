"""
Memory layer for the AI Engineering Bootcamp mini-framework.

This module is intentionally implemented with the Python standard library only.
It is not a vector database. It models the engineering contract of a memory
layer: namespaces, visibility, TTL, auditability, snapshots and deterministic
retrieval. A production implementation can later replace the in-memory store
with PostgreSQL, Redis, a vector database or an MCP-backed store without
changing the public contract.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
import json
import re
import uuid
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set


VALID_VISIBILITIES = {"private", "shared", "public"}
VALID_KINDS = {
    "conversation",
    "preference",
    "fact",
    "task_state",
    "tool_observation",
    "policy",
}


def utc_now() -> datetime:
    """Return an aware UTC datetime."""

    return datetime.now(timezone.utc)


def parse_datetime(value: Optional[str]) -> Optional[datetime]:
    """Parse an ISO datetime produced by this module."""

    if value is None:
        return None
    return datetime.fromisoformat(value)


def to_iso(value: Optional[datetime]) -> Optional[str]:
    """Serialize an aware datetime to ISO 8601."""

    if value is None:
        return None
    return value.isoformat()


def tokenize(text: str) -> Set[str]:
    """Small deterministic tokenizer used for educational retrieval scoring."""

    return set(re.findall(r"[a-zA-Z0-9_]+", text.lower()))


def redact_pii(text: str) -> str:
    """Redact common email addresses and phone-like numbers.

    This is deliberately conservative and educational. Production PII handling
    should use a dedicated classifier, policy engine and audit flow.
    """

    text = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[REDACTED_EMAIL]", text)
    text = re.sub(r"\b(?:\+?\d[\d\s.-]{7,}\d)\b", "[REDACTED_PHONE]", text)
    return text


@dataclass(frozen=True)
class MemoryRecord:
    """Immutable memory record stored by the memory layer."""

    id: str
    namespace: str
    owner_agent: str
    kind: str
    content: str
    visibility: str = "private"
    tags: List[str] = field(default_factory=list)
    importance: float = 0.5
    created_at: str = field(default_factory=lambda: to_iso(utc_now()))
    updated_at: str = field(default_factory=lambda: to_iso(utc_now()))
    expires_at: Optional[str] = None
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self, now: Optional[datetime] = None) -> bool:
        """Return True when this record is expired at ``now``."""

        if self.expires_at is None:
            return False
        now = now or utc_now()
        return parse_datetime(self.expires_at) <= now

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryRecord":
        """Build a record from a JSON dictionary."""

        return cls(**data)


@dataclass(frozen=True)
class MemoryQuery:
    """Query contract for deterministic memory retrieval."""

    namespace: str
    text: str = ""
    requester_agent: str = "agent"
    allowed_visibility: Sequence[str] = ("private", "shared", "public")
    tags_any: Sequence[str] = ()
    tags_all: Sequence[str] = ()
    kinds: Sequence[str] = ()
    min_importance: float = 0.0
    limit: int = 5
    now: Optional[datetime] = None
    include_expired: bool = False


@dataclass(frozen=True)
class MemorySearchResult:
    """Search result containing a record and its deterministic score."""

    record: MemoryRecord
    score: float
    reasons: List[str]


class MemoryStore:
    """In-memory store implementing the memory layer contract.

    The store is deliberately small but production-shaped:
    - namespace isolation prevents cross-user or cross-tenant leakage;
    - visibility controls what can be injected into context;
    - TTL supports short-lived memories;
    - snapshots make persistence boundaries explicit;
    - audit events make updates inspectable.
    """

    def __init__(self) -> None:
        self._records: Dict[str, MemoryRecord] = {}
        self._audit_log: List[Dict[str, Any]] = []

    def add(
        self,
        *,
        namespace: str,
        owner_agent: str,
        kind: str,
        content: str,
        visibility: str = "private",
        tags: Optional[Iterable[str]] = None,
        importance: float = 0.5,
        ttl_seconds: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
        now: Optional[datetime] = None,
        redact: bool = True,
    ) -> MemoryRecord:
        """Add a memory record after validating policy-related fields."""

        if not namespace:
            raise ValueError("namespace is required")
        if not owner_agent:
            raise ValueError("owner_agent is required")
        if kind not in VALID_KINDS:
            raise ValueError(f"invalid memory kind: {kind}")
        if visibility not in VALID_VISIBILITIES:
            raise ValueError(f"invalid visibility: {visibility}")
        if not 0 <= importance <= 1:
            raise ValueError("importance must be between 0 and 1")

        now = now or utc_now()
        expires_at = to_iso(now + timedelta(seconds=ttl_seconds)) if ttl_seconds else None
        clean_content = redact_pii(content) if redact else content

        record = MemoryRecord(
            id=str(uuid.uuid4()),
            namespace=namespace,
            owner_agent=owner_agent,
            kind=kind,
            content=clean_content,
            visibility=visibility,
            tags=sorted({tag.strip().lower() for tag in (tags or []) if tag.strip()}),
            importance=importance,
            created_at=to_iso(now),
            updated_at=to_iso(now),
            expires_at=expires_at,
            metadata=dict(metadata or {}),
        )
        self._records[record.id] = record
        self._audit("add", record, now=now)
        return record

    def update(
        self,
        record_id: str,
        *,
        content: Optional[str] = None,
        tags: Optional[Iterable[str]] = None,
        importance: Optional[float] = None,
        metadata_patch: Optional[Dict[str, Any]] = None,
        now: Optional[datetime] = None,
    ) -> MemoryRecord:
        """Update selected record fields while preserving identity."""

        record = self._require(record_id)
        now = now or utc_now()

        if importance is not None and not 0 <= importance <= 1:
            raise ValueError("importance must be between 0 and 1")

        metadata = dict(record.metadata)
        if metadata_patch:
            metadata.update(metadata_patch)

        updated = MemoryRecord(
            id=record.id,
            namespace=record.namespace,
            owner_agent=record.owner_agent,
            kind=record.kind,
            content=redact_pii(content) if content is not None else record.content,
            visibility=record.visibility,
            tags=sorted({tag.strip().lower() for tag in (tags if tags is not None else record.tags) if tag.strip()}),
            importance=importance if importance is not None else record.importance,
            created_at=record.created_at,
            updated_at=to_iso(now),
            expires_at=record.expires_at,
            version=record.version + 1,
            metadata=metadata,
        )
        self._records[record_id] = updated
        self._audit("update", updated, now=now)
        return updated

    def delete(self, record_id: str, *, now: Optional[datetime] = None) -> None:
        """Delete a single memory record."""

        record = self._require(record_id)
        del self._records[record_id]
        self._audit("delete", record, now=now or utc_now())

    def forget_namespace(self, namespace: str, *, now: Optional[datetime] = None) -> int:
        """Delete all memories for a namespace and return the count."""

        ids = [record_id for record_id, record in self._records.items() if record.namespace == namespace]
        for record_id in ids:
            record = self._records.pop(record_id)
            self._audit("forget", record, now=now or utc_now())
        return len(ids)

    def list_records(
        self,
        *,
        namespace: Optional[str] = None,
        include_expired: bool = False,
        now: Optional[datetime] = None,
    ) -> List[MemoryRecord]:
        """List records with optional namespace and expiration filtering."""

        now = now or utc_now()
        records = list(self._records.values())
        if namespace is not None:
            records = [record for record in records if record.namespace == namespace]
        if not include_expired:
            records = [record for record in records if not record.is_expired(now)]
        return sorted(records, key=lambda record: (record.namespace, record.created_at, record.id))

    def retrieve(self, query: MemoryQuery) -> List[MemorySearchResult]:
        """Retrieve memories matching a query.

        The scoring model is transparent for teaching:
        - lexical overlap with ``query.text``;
        - tag overlap;
        - importance;
        - small boost when the requester owns the record.
        """

        if query.limit <= 0:
            return []

        query_terms = tokenize(query.text)
        allowed = set(query.allowed_visibility)
        tags_any = {tag.lower() for tag in query.tags_any}
        tags_all = {tag.lower() for tag in query.tags_all}
        kinds = set(query.kinds)
        now = query.now or utc_now()

        results: List[MemorySearchResult] = []
        for record in self._records.values():
            if record.namespace != query.namespace:
                continue
            if not query.include_expired and record.is_expired(now):
                continue
            if record.visibility not in allowed:
                continue
            if kinds and record.kind not in kinds:
                continue
            if record.importance < query.min_importance:
                continue

            record_tags = set(record.tags)
            if tags_any and not (record_tags & tags_any):
                continue
            if tags_all and not tags_all.issubset(record_tags):
                continue

            content_terms = tokenize(record.content)
            overlap = query_terms & content_terms
            tag_overlap = query_terms & record_tags
            score = record.importance
            reasons = [f"importance={record.importance:.2f}"]

            if query_terms:
                lexical = len(overlap) / max(len(query_terms), 1)
                score += lexical * 2
                if overlap:
                    reasons.append("lexical_overlap=" + ",".join(sorted(overlap)))

            if tag_overlap:
                score += len(tag_overlap) * 1.2
                reasons.append("tag_overlap=" + ",".join(sorted(tag_overlap)))

            if record.owner_agent == query.requester_agent:
                score += 0.25
                reasons.append("same_owner_agent")

            results.append(MemorySearchResult(record=record, score=round(score, 4), reasons=reasons))

        results.sort(key=lambda item: (item.score, item.record.updated_at), reverse=True)
        return results[: query.limit]

    def promote_event(
        self,
        *,
        namespace: str,
        owner_agent: str,
        event_text: str,
        event_type: str,
        now: Optional[datetime] = None,
    ) -> Optional[MemoryRecord]:
        """Promote an event into durable memory when it looks reusable.

        This intentionally simple heuristic demonstrates the engineering
        boundary: not every message becomes memory.
        """

        lowered = event_text.lower()
        if event_type == "user_feedback" and ("prefer" in lowered or "préfère" in lowered):
            return self.add(
                namespace=namespace,
                owner_agent=owner_agent,
                kind="preference",
                content=event_text,
                visibility="private",
                tags=["preference", "feedback"],
                importance=0.85,
                now=now,
            )
        if event_type == "verified_fact":
            return self.add(
                namespace=namespace,
                owner_agent=owner_agent,
                kind="fact",
                content=event_text,
                visibility="shared",
                tags=["fact", "verified"],
                importance=0.75,
                now=now,
            )
        return None

    def snapshot(self) -> Dict[str, Any]:
        """Return a JSON-serializable snapshot of records and audit log."""

        return {
            "schema_version": "1.0",
            "records": [record.to_dict() for record in self.list_records(include_expired=True)],
            "audit_log": list(self._audit_log),
        }

    @classmethod
    def from_snapshot(cls, snapshot: Dict[str, Any]) -> "MemoryStore":
        """Load a memory store from a snapshot."""

        if snapshot.get("schema_version") != "1.0":
            raise ValueError("unsupported snapshot schema_version")
        store = cls()
        store._records = {
            data["id"]: MemoryRecord.from_dict(data)
            for data in snapshot.get("records", [])
        }
        store._audit_log = list(snapshot.get("audit_log", []))
        return store

    def to_json(self) -> str:
        """Serialize the snapshot as indented JSON."""

        return json.dumps(self.snapshot(), ensure_ascii=False, indent=2, sort_keys=True)

    @property
    def audit_log(self) -> List[Dict[str, Any]]:
        """Return a copy of the audit log."""

        return list(self._audit_log)

    def _require(self, record_id: str) -> MemoryRecord:
        try:
            return self._records[record_id]
        except KeyError as exc:
            raise KeyError(f"unknown memory record: {record_id}") from exc

    def _audit(self, action: str, record: MemoryRecord, *, now: datetime) -> None:
        self._audit_log.append(
            {
                "action": action,
                "record_id": record.id,
                "namespace": record.namespace,
                "owner_agent": record.owner_agent,
                "visibility": record.visibility,
                "version": record.version,
                "at": to_iso(now),
            }
        )
