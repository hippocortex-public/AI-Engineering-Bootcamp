# Références — MCP Client

## Références principales

- Model Context Protocol — Tools specification.
- Model Context Protocol — Streamable HTTP transport.
- OpenAI Agents SDK — MCP integration.
- OpenAI Agents SDK — MCP server abstractions.
- JSON-RPC 2.0 specification.

## À retenir

Le client MCP est une couche d'adaptation.

Il transforme des capacités exposées par un serveur en outils sûrs, validés, traçables et utilisables par un agent.

## Lectures recommandées

- Documentation officielle MCP : tools, resources, prompts et transport.
- Documentation OpenAI Agents SDK : intégration MCP et runners agentiques.
- Bonnes pratiques JSON Schema pour l'interface entre modèles et systèmes.
- Bonnes pratiques d'observabilité : traces, événements, statuts et erreurs.

## Notes pédagogiques

Le lab n'implémente pas tout le protocole MCP.

Il se concentre sur le minimum utile pour comprendre le rôle d'un client :

- requêtes JSON-RPC ;
- initialisation ;
- découverte ;
- validation ;
- appel ;
- erreurs ;
- adaptation agentique.
