# Lab — MCP Client

## Objectif

Construire un client MCP minimal capable de découvrir des tools, valider les arguments, appeler un serveur simulé et exposer les tools à un agent.

## Fichiers

```text
mcp_client.py
test_mcp_client.py
```

## Exécution

```bash
python -m py_compile mcp_client.py test_mcp_client.py
python test_mcp_client.py
```

## Contraintes

- Python standard library uniquement.
- Aucun appel réseau.
- Transport JSON-RPC simulé en mémoire.
- Séparation entre client MCP, serveur simulé et logique agentique.

## Extension proposée

Ajoute un second serveur simulé et construis un client capable de fusionner plusieurs registries d'outils.
