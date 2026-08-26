# Corrigé — Challenge MCP Client

## Approche

Une solution robuste doit séparer :

1. le transport JSON-RPC ;
2. la découverte des tools ;
3. la validation ;
4. la politique de sécurité ;
5. l'adaptation en registry agentique.

## Exemple de flux

```python
transport = InMemoryTransport(InMemoryMCPServer())
client = MCPClient(transport)

client.initialize()
tools = client.list_tools()
result = client.call_tool("get_ticket", {"ticket_id": "INC-42"})
```

## Points de validation attendus

- `initialize` doit être appelé avant les tools.
- `tools/list` doit retourner des définitions exploitables.
- `tools/call` doit refuser les arguments invalides.
- `refund_customer` doit être bloqué sans `approved=True`.
- les traces doivent conserver les succès et les erreurs.

## Améliorations possibles

- Ajouter un TTL au cache.
- Masquer les champs sensibles dans les traces.
- Ajouter un budget d'appels par session.
- Supporter plusieurs serveurs MCP.
- Associer chaque tool à une politique d'autorisation.
