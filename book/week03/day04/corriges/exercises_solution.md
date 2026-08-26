# Corrigé — Exercices MCP Client

## Exercice 1 — Responsabilités

| Responsabilité | Couche |
|---|---|
| Choisir le prochain outil à appeler | Agent |
| Retourner la liste des tools exposés | MCP Server |
| Valider localement les arguments | MCP Client |
| Exécuter une recherche dans une base support | Tool métier |
| Transformer un tool MCP en fonction Python appelable | MCP Client |
| Bloquer un outil sensible sans approbation | MCP Client ou guardrail |
| Synthétiser la réponse finale à l'utilisateur | Agent |

## Exercice 2 — Schéma

Champs obligatoires :

- `customer_id`
- `priority`

Types :

- `customer_id`: string
- `priority`: string
- `include_history`: boolean

Propriétés supplémentaires :

- interdites, car `additionalProperties` vaut `false`.

Exemple valide :

```json
{
  "customer_id": "CUST-42",
  "priority": "high",
  "include_history": true
}
```

Exemple invalide :

```json
{
  "customer_id": "CUST-42",
  "priority": "high",
  "debug": true
}
```

La propriété `debug` n'est pas déclarée.

## Exercice 3 — Trace

```json
{
  "request_id": 7,
  "tool": "get_ticket",
  "arguments": {"ticket_id": "INC-42"},
  "status": "success",
  "duration_ms": 12,
  "error": null
}
```

## Exercice 4 — Adapter MCP vers agent

```python
def as_agent_tool(client, tool_name):
    def tool(arguments):
        return client.call_tool(tool_name, arguments)
    return tool
```

## Exercice 5 — Cache

Le cache doit être invalidable car le serveur peut évoluer.

Situations dangereuses :

1. un tool a été supprimé ou renommé ;
2. un schéma d'entrée a changé ;
3. une permission a été modifiée ;
4. un tool sensible a été ajouté ;
5. une version serveur différente est déployée.

## Exercice 6 — Sécurité

Contrôles possibles avant `refund_customer` :

- vérifier une approbation humaine ;
- contrôler un montant maximum ;
- vérifier le rôle utilisateur ;
- journaliser l'appel ;
- exiger un ticket associé ;
- bloquer l'appel si le contexte est incomplet.
