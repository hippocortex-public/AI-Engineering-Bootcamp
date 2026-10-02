import hashlib
import json
from dataclasses import dataclass

import psycopg
import redis

from .auth import Principal


class BackendUnavailable(Exception):
    pass


class DocumentNotFound(Exception):
    pass


class PermissionDenied(Exception):
    pass


class RateLimited(Exception):
    def __init__(self, retry_after):
        self.retry_after = max(1, int(retry_after))


def require_scope(principal: Principal, scope: str):
    if scope not in principal.scopes:
        raise PermissionDenied


@dataclass(frozen=True)
class Document:
    document_id: str
    content: str


class PgRepository:
    def __init__(self, settings):
        self.settings = settings

    def connect(self):
        return psycopg.connect(host=self.settings.pg_host, dbname=self.settings.pg_db,
            user=self.settings.pg_user, password=self.settings.pg_password,
            connect_timeout=3, options="-c statement_timeout=2000")

    def ready(self):
        try:
            with self.connect() as connection:
                row = connection.execute("SELECT version FROM schema_version").fetchone()
            return row is not None and row[0] == 1
        except psycopg.Error:
            return False

    def get(self, principal, document_id):
        require_scope(principal, "documents:read")
        try:
            with self.connect() as connection:
                row = connection.execute(
                    "SELECT document_id, content FROM documents WHERE tenant_id = %s AND document_id = %s",
                    (principal.tenant, document_id),
                ).fetchone()
        except psycopg.Error:
            raise BackendUnavailable from None
        if row is None:
            raise DocumentNotFound
        return Document(*row)


RATE_SCRIPT = """
local count = tonumber(redis.call('GET', KEYS[1]) or '0')
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
if count >= limit then
    local ttl = redis.call('TTL', KEYS[1])
    if ttl < 1 then ttl = 1 end
    return {0, ttl}
end
count = redis.call('INCR', KEYS[1])
if count == 1 then redis.call('EXPIRE', KEYS[1], window) end
return {1, redis.call('TTL', KEYS[1])}
"""


class RedisBackend:
    def __init__(self, client, limit=10, window=60):
        if limit < 1 or window < 1:
            raise ValueError("Invalid rate limit")
        self.client, self.limit, self.window = client, limit, window

    @classmethod
    def from_settings(cls, settings):
        return cls(redis.Redis(host=settings.redis_host, password=settings.redis_password,
            decode_responses=True, socket_connect_timeout=2, socket_timeout=2))

    def ready(self):
        try:
            return bool(self.client.ping())
        except redis.RedisError:
            return False

    def consume(self, principal):
        key = f"quota:{principal.tenant}:{principal.subject}"
        try:
            allowed, retry_after = self.client.eval(RATE_SCRIPT, 1, key, self.limit, self.window)
        except redis.RedisError:
            # Redis porte une limite de sécurité ; ne pas ignorer son indisponibilité.
            raise BackendUnavailable from None
        if not allowed:
            raise RateLimited(retry_after)

    @staticmethod
    def cache_key(principal, message, document):
        payload = json.dumps({"message": message,
            "document_id": document.document_id if document else None,
            "content": document.content if document else None}, sort_keys=True)
        digest = hashlib.sha256(payload.encode()).hexdigest()
        return f"answer:v1:{principal.tenant}:{principal.subject}:{digest}"

    def get_answer(self, key):
        try:
            return self.client.get(key)
        except redis.RedisError:
            raise BackendUnavailable from None

    def put_answer(self, key, answer):
        try:
            self.client.set(key, answer, ex=120)
        except redis.RedisError:
            raise BackendUnavailable from None
