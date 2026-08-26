# Références — Sharing State

## Références principales

- OpenAI Agents SDK — Sessions, Memory et continuité de conversation.
- OpenAI Agents SDK — MCP integration.
- Model Context Protocol Specification — Resources.
- Model Context Protocol Specification — Tools.
- JSON-RPC 2.0 Specification.

## Concepts à revoir

- conversation state ;
- memory ;
- shared state ;
- event sourcing ;
- compare-and-set ;
- optimistic concurrency control ;
- handoff ;
- least privilege ;
- traceability.

## À retenir

Le sharing state est un contrat de coordination.

Il ne doit pas être confondu avec :

- le prompt ;
- la mémoire long terme ;
- le cache d'outils ;
- les ressources MCP ;
- les logs bruts.

## Lectures complémentaires

- Patterns d'orchestration multi-agent.
- Event sourcing appliqué aux workflows.
- Conception d'API idempotentes.
- Contrôle d'accès par ressource.
- Observabilité des systèmes agentiques.
