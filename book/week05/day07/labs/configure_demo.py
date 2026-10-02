"""Génère les secrets locaux sans les imprimer ; aucune rotation implicite."""
import json
import os
from pathlib import Path
import secrets


def main():
    folder = Path(__file__).resolve().parent / "secrets"
    # mkdir sans exist_ok : ne pas remplacer des mots de passe d'une base existante.
    folder.mkdir(mode=0o700)
    identities = [
        {"subject": "alice", "tenant": "alpha", "scopes": ["chat:write", "documents:read"]},
        {"subject": "bob", "tenant": "beta", "scopes": ["chat:write", "documents:read"]},
        {"subject": "operator", "tenant": "platform", "scopes": ["metrics:read"]},
    ]
    for identity in identities:
        identity["api_key"] = secrets.token_urlsafe(32)
    payloads = {"db_admin_password": secrets.token_urlsafe(32),
        "db_app_password": secrets.token_urlsafe(32), "redis_password": secrets.token_urlsafe(32),
        "api_identities.json": json.dumps(identities, indent=2)}
    for name, content in payloads.items():
        path = folder / name
        path.write_text(content + "\n")
        # Secrets file-based Compose : lisibles par UID 10001 au montage.
        # Le dossier parent privé 0700 protège les fichiers côté hôte Unix.
        os.chmod(path, 0o444)
    print("Secrets locaux créés ; aucune valeur affichée.")


if __name__ == "__main__":
    main()
