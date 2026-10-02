import json
from types import SimpleNamespace
from unittest.mock import MagicMock

import psycopg
import pytest

from deployment_ai_service.auth import Principal
from deployment_ai_service.settings import Settings
from deployment_ai_service.storage import BackendUnavailable, DocumentNotFound, PgRepository


def principal():
    return Principal("alice", "alpha", frozenset({"documents:read"}))


def test_sql_is_parameterized_and_tenant_scoped(monkeypatch):
    repository = PgRepository(None)
    connection = MagicMock()
    connection.execute.return_value.fetchone.return_value = ("guide", "data")
    context = MagicMock()
    context.__enter__.return_value = connection
    monkeypatch.setattr(repository, "connect", lambda: context)
    document = repository.get(principal(), "' OR 1=1 --")
    sql, params = connection.execute.call_args.args
    assert "tenant_id = %s AND document_id = %s" in sql
    assert "OR 1=1" not in sql
    assert params == ("alpha", "' OR 1=1 --")
    assert document.content == "data"


def test_absent_row_is_not_found(monkeypatch):
    repository = PgRepository(None)
    context = MagicMock()
    context.__enter__.return_value.execute.return_value.fetchone.return_value = None
    monkeypatch.setattr(repository, "connect", lambda: context)
    with pytest.raises(DocumentNotFound):
        repository.get(principal(), "beta-guide")


def test_database_failure_is_sanitized(monkeypatch):
    def fail():
        raise psycopg.OperationalError("SECRET_DSN")
    repository = PgRepository(None)
    monkeypatch.setattr(repository, "connect", fail)
    assert repository.ready() is False
    with pytest.raises(BackendUnavailable) as exc:
        repository.get(principal(), "guide")
    assert "SECRET_DSN" not in str(exc.value)


@pytest.mark.parametrize("schema_version,ready", [(1, True), (2, False), (None, False)])
def test_readiness_checks_schema_version(monkeypatch, schema_version, ready):
    repository = PgRepository(None)
    context = MagicMock()
    context.__enter__.return_value.execute.return_value.fetchone.return_value = (schema_version,) if schema_version else None
    monkeypatch.setattr(repository, "connect", lambda: context)
    assert repository.ready() is ready


def test_secret_configuration_loads_without_exposing_passwords(tmp_path, monkeypatch):
    values = {
        "AUTH_IDENTITIES_FILE": json.dumps([{"api_key": "a" * 40, "subject": "alice", "tenant": "alpha", "scopes": ["chat:write"]}]),
        "PG_PASSWORD_FILE": "PRIVATE_DB_PASSWORD",
        "REDIS_PASSWORD_FILE": "PRIVATE_REDIS_PASSWORD",
    }
    for name, value in values.items():
        path = tmp_path / name
        path.write_text(value)
        monkeypatch.setenv(name, str(path))
    settings = Settings.from_environment()
    assert settings.pg_password == "PRIVATE_DB_PASSWORD"
    assert "PRIVATE_DB_PASSWORD" not in repr(settings)
    assert "PRIVATE_REDIS_PASSWORD" not in repr(settings)


def test_missing_secrets_fail_closed(monkeypatch):
    monkeypatch.delenv("AUTH_IDENTITIES_FILE", raising=False)
    with pytest.raises(RuntimeError, match="Invalid deployment configuration"):
        Settings.from_environment()
