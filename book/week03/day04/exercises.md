# Exercices — MCP Client

## Exercice 1 — Identifier les responsabilités

Classe les responsabilités suivantes dans la bonne couche :

1. Choisir le prochain outil à appeler.
2. Retourner la liste des tools exposés.
3. Valider localement les arguments.
4. Exécuter une recherche dans une base support.
5. Transformer un tool MCP en fonction Python appelable.
6. Bloquer un outil sensible sans approbation.
7. Synthétiser la réponse finale à l'utilisateur.

Couches possibles :

- Agent
- MCP Client
- MCP Server
- Tool métier

## Exercice 2 — Lire un schéma de tool

À partir du schéma suivant, indique :

- les champs obligatoires ;
- les types attendus ;
- si des propriétés supplémentaires sont autorisées ;
- un exemple d'appel valide ;
- un exemple d'appel invalide.

```json
{
  "type": "object",
  "required": ["customer_id", "priority"],
  "properties": {
    "customer_id": {"type": "string"},
    "priority": {"type": "string"},
    "include_history": {"type": "boolean"}
  },
  "additionalProperties": false
}
```

## Exercice 3 — Concevoir une trace

Propose une structure JSON pour tracer un appel MCP contenant :

- identifiant de requête ;
- nom du tool ;
- arguments ;
- statut ;
- durée approximative ;
- erreur éventuelle.

## Exercice 4 — Adapter MCP vers agent

Écris une fonction `as_agent_tool(client, tool_name)` qui retourne une fonction Python prenant `arguments` et appelant `client.call_tool`.

Pseudo-interface attendue :

```python
tool = as_agent_tool(client, "get_ticket")
result = tool({"ticket_id": "INC-42"})
```

## Exercice 5 — Cache

Explique pourquoi le cache de `tools/list` doit être invalidable.

Donne deux situations où le cache peut devenir dangereux.

## Exercice 6 — Sécurité

Un serveur expose un tool `refund_customer`.

Propose trois contrôles à appliquer côté client avant d'autoriser l'appel.
