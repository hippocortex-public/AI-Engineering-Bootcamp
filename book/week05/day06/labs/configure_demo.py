"""Crée une configuration privée locale sans afficher les clés."""
import json
import os
import secrets
from pathlib import Path


def main() -> None:
    path = Path(__file__).resolve().parent / ".demo-identities.json"
    identities = [
        {"subject": "alice", "tenant": "alpha", "scopes": ["chat:write", "documents:read", "tools:read"]},
        {"subject": "bob", "tenant": "beta", "scopes": ["chat:write", "documents:read", "tools:read"]},
        {"subject": "carol", "tenant": "alpha", "scopes": ["chat:write"]},
    ]
    for identity in identities:
        identity["api_key"] = secrets.token_urlsafe(32)
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        raise SystemExit("Configuration déjà présente ; aucun écrasement effectué.") from None
    with os.fdopen(fd, "w", encoding="utf-8") as output:
        json.dump(identities, output, indent=2)
        output.write("\n")
    print("Configuration locale créée. Aucune clé affichée.")


if __name__ == "__main__":
    main()
