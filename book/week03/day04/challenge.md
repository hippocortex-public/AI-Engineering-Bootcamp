# Challenge — Construire un client MCP robuste

## Contexte

Tu développes un assistant support interne. Le serveur MCP expose trois tools :

1. `get_ticket`
2. `search_knowledge_base`
3. `refund_customer`

Le troisième tool est sensible.

## Objectif

Implémente ou complète un client MCP capable de :

- initialiser une session ;
- découvrir les tools ;
- mettre en cache la liste ;
- valider les arguments ;
- appeler un tool ;
- refuser `refund_customer` sans approbation explicite ;
- retourner une trace JSON.

## Contraintes

- Ne pas utiliser de dépendance externe.
- Ne pas appeler un vrai réseau.
- Utiliser un transport simulé en mémoire.
- Garder la logique agentique séparée de la logique protocolaire.
- Produire des erreurs lisibles.

## Entrée attendue

```python
client.initialize()
tools = client.list_tools()

result = client.call_tool(
    "get_ticket",
    {"ticket_id": "INC-42"}
)
```

## Sortie attendue

```python
{
  "tool": "get_ticket",
  "is_error": false,
  "structured_content": {
    "ticket_id": "INC-42",
    "status": "open"
  }
}
```

## Bonus

Ajoute une méthode :

```python
client.as_agent_tools()
```

Elle doit retourner un dictionnaire :

```python
{
  "get_ticket": callable,
  "search_knowledge_base": callable,
  "refund_customer": callable
}
```
