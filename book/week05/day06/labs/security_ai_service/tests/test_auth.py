import json

import pytest

from security_ai_service.auth import Credential, IdentityStore, Principal
from conftest import ALPHA_KEY, ALL_SCOPES


@pytest.mark.parametrize("value", [None, "", "[]", "{}", "not-json", '[{"api_key":"DO_NOT_LEAK"}]'])
def test_invalid_configuration_fails_closed(monkeypatch, value):
    if value is None:
        monkeypatch.delenv("SECURITY_IDENTITIES_JSON", raising=False)
    else:
        monkeypatch.setenv("SECURITY_IDENTITIES_JSON", value)
    with pytest.raises(RuntimeError, match="Invalid or missing") as exc:
        IdentityStore.from_environment()
    assert "DO_NOT_LEAK" not in str(exc.value)


def test_valid_configuration_and_key_rotation(monkeypatch):
    monkeypatch.setenv("SECURITY_IDENTITIES_JSON", json.dumps([{
        "api_key": ALPHA_KEY, "subject": "alice", "tenant": "alpha", "scopes": ["chat:write"],
    }]))
    store = IdentityStore.from_environment()
    assert store.authenticate(ALPHA_KEY).tenant == "alpha"
    assert store.authenticate("z" * 40) is None
    assert store.authenticate("é" * 40) is None


def test_duplicate_keys_fail():
    credential = Credential(ALPHA_KEY, Principal("alice", "alpha", ALL_SCOPES))
    with pytest.raises(ValueError, match="Duplicate"):
        IdentityStore([credential, credential])
    assert ALPHA_KEY not in repr(credential)


@pytest.mark.parametrize("subject,tenant,scopes", [
    ("alice\nadmin", "alpha", ALL_SCOPES),
    ("alice", "../beta", ALL_SCOPES),
    ("alice", "alpha", frozenset({"admin:*"})),
])
def test_invalid_principals_rejected(subject, tenant, scopes):
    with pytest.raises(ValueError):
        Principal(subject, tenant, scopes)
