# Lab — MCP Server pédagogique

Ce lab implémente un serveur MCP minimal en Python standard library.

## Fichiers

- `mcp_server.py` : serveur MCP pédagogique ;
- `test_mcp_server.py` : tests unitaires sans dépendance externe.

## Lancer le lab

```bash
python mcp_server.py
python test_mcp_server.py
```

## Ce que le lab démontre

- initialisation ;
- discovery des tools ;
- appel d’outil ;
- lecture de resource ;
- récupération de prompt ;
- erreurs JSON-RPC ;
- validation d’arguments ;
- garde-fou sur tool sensible ;
- trace d’exécution.

## Limite volontaire

Ce lab ne met pas en œuvre de transport réseau MCP réel. Il se concentre sur les responsabilités serveur.
