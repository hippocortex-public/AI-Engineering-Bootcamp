import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from .auth import Credential, IdentityStore, Principal


def read_secret(path: str) -> str:
    value = Path(path).read_text(encoding="utf-8").strip()
    if not value:
        raise ValueError("Empty secret")
    return value


@dataclass(frozen=True)
class Settings:
    pg_host: str
    pg_db: str
    pg_user: str
    pg_password: str = field(repr=False)
    redis_host: str
    redis_password: str = field(repr=False)
    identities: IdentityStore = field(repr=False)
    release: str = "local"

    @classmethod
    def from_environment(cls):
        try:
            raw = json.loads(read_secret(os.environ["AUTH_IDENTITIES_FILE"]))
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
                credentials.append(Credential(item["api_key"], Principal(item["subject"], item["tenant"], frozenset(item["scopes"]))))
            return cls(
                os.getenv("PG_HOST", "db"), os.getenv("PG_DB", "bootcamp"),
                os.getenv("PG_USER", "bootcamp_app"), read_secret(os.environ["PG_PASSWORD_FILE"]),
                os.getenv("REDIS_HOST", "redis"), read_secret(os.environ["REDIS_PASSWORD_FILE"]),
                IdentityStore(credentials), os.getenv("APP_RELEASE", "local"),
            )
        except (OSError, ValueError, TypeError, KeyError):
            raise RuntimeError("Invalid deployment configuration") from None
