from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
from dataclasses import dataclass, field

KNOWN_SCOPES = frozenset({"chat:write", "documents:read", "tools:read", "metrics:read"})
IDENTIFIER = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}")


@dataclass(frozen=True)
class Principal:
    subject: str
    tenant: str
    scopes: frozenset[str]

    def __post_init__(self) -> None:
        if not IDENTIFIER.fullmatch(self.subject) or not IDENTIFIER.fullmatch(self.tenant):
            raise ValueError("Invalid principal identifier")
        if not isinstance(self.scopes, frozenset) or not self.scopes <= KNOWN_SCOPES:
            raise ValueError("Invalid scopes")


@dataclass(frozen=True)
class Credential:
    api_key: str = field(repr=False)
    principal: Principal


class IdentityStore:
    """Identités injectées par configuration ; aucun accès anonyme de secours."""

    def __init__(self, credentials: list[Credential]) -> None:
        if not credentials:
            raise ValueError("At least one identity is required")
        self._entries: list[tuple[bytes, Principal]] = []
        seen: set[bytes] = set()
        for credential in credentials:
            key = credential.api_key
            if not isinstance(key, str) or not key.isascii() or not 32 <= len(key) <= 128:
                raise ValueError("API keys must contain 32 to 128 ASCII characters")
            digest = hashlib.sha256(key.encode()).digest()
            if digest in seen:
                raise ValueError("Duplicate API key")
            seen.add(digest)
            self._entries.append((digest, credential.principal))

    def authenticate(self, api_key: str | None) -> Principal | None:
        if api_key is None or not api_key.isascii() or not 32 <= len(api_key) <= 128:
            return None
        digest = hashlib.sha256(api_key.encode()).digest()
        principal = None
        for expected, candidate in self._entries:
            # Empreintes de taille fixe ; pas de comparaison de chaînes via ==.
            if hmac.compare_digest(expected, digest):
                principal = candidate
        return principal

    @classmethod
    def from_environment(cls) -> IdentityStore:
        try:
            raw = json.loads(os.environ["SECURITY_IDENTITIES_JSON"])
            if not isinstance(raw, list):
                raise ValueError
            credentials = []
            for item in raw:
                if not isinstance(item, dict) or set(item) != {"api_key", "subject", "tenant", "scopes"}:
                    raise ValueError
                if not isinstance(item["scopes"], list) or not all(isinstance(s, str) for s in item["scopes"]):
                    raise ValueError
                if not isinstance(item["subject"], str) or not isinstance(item["tenant"], str):
                    raise ValueError
                principal = Principal(item["subject"], item["tenant"], frozenset(item["scopes"]))
                credentials.append(Credential(item["api_key"], principal))
            return cls(credentials)
        except (KeyError, ValueError, TypeError):
            # Ne pas inclure le JSON, la clé ni la cause dans le message exposé.
            raise RuntimeError("Invalid or missing SECURITY_IDENTITIES_JSON") from None
