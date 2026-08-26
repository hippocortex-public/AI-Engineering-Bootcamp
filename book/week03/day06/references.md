# Références — Jour 6 — Context Engineering

## Documentation principale

- OpenAI Agents SDK — Context management  
  https://openai.github.io/openai-agents-python/context/

- OpenAI Agents SDK — Sessions  
  https://openai.github.io/openai-agents-python/sessions/

- OpenAI Agents SDK — MCP  
  https://openai.github.io/openai-agents-python/mcp/

- Model Context Protocol — Overview  
  https://modelcontextprotocol.io/specification/2025-06-18/server/index

- Model Context Protocol — Resources  
  https://modelcontextprotocol.io/specification/2025-06-18/server/resources

- Model Context Protocol — Tools  
  https://modelcontextprotocol.io/specification/2025-06-18/server/tools

## À retenir

Ces références ne remplacent pas le lab. Elles servent à relier l’implémentation pédagogique aux concepts utilisés en production :

- contexte d’exécution ;
- sessions ;
- ressources ;
- outils ;
- MCP ;
- sélection et transmission contrôlée du contexte.

## Notes pédagogiques

Le lab utilise uniquement la Python standard library pour rester reproductible.

En production, l’équipe devra compléter ce moteur avec :

- tokenizer exact du modèle ;
- recherche sémantique ;
- permissions réelles ;
- journal d’audit ;
- classification de données sensibles ;
- observabilité.
