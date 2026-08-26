# Corrigé — Challenge

## Implémentation indicative

```python
def classify_issue(arguments, context):
    message = arguments["message"].lower()
    if "invoice" in message or "billing" in message:
        return {"category": "billing", "confidence": 0.82}
    if "password" in message or "breach" in message:
        return {"category": "security", "confidence": 0.86}
    if "error" in message or "bug" in message:
        return {"category": "technical", "confidence": 0.78}
    return {"category": "other", "confidence": 0.55}
```

Schéma :

```json
{
  "type": "object",
  "properties": {
    "message": {
      "type": "string"
    }
  },
  "required": ["message"],
  "additionalProperties": false
}
```

Pour `create_ticket`, le point important est moins le code métier que la politique :

```python
registry.register(
    "create_ticket",
    "Crée un ticket support après validation humaine.",
    create_ticket_schema,
    create_ticket,
    sensitive=True,
    required_scope="ticket:write",
    tags=["support", "sensitive"],
)
```

## Tests attendus

- `registry.list_tools()` ne contient pas `create_ticket` ;
- `registry.list_tools(include_sensitive=True)` contient `create_ticket` ;
- contexte sans scope : résultat `blocked` ;
- contexte avec scope mais sans approbation : résultat `blocked` ;
- contexte avec scope et approbation : résultat `completed` ;
- catégorie hors enum : résultat `failed` ;
- chaque résultat contient `trace`.

## Exemple de filtre par rôle

```python
ROLE_TAGS = {
    "support_reader": {"knowledge"},
    "support_operator": {"knowledge", "support"},
    "admin": {"knowledge", "support", "sensitive"},
}

def list_tools_for_agent(registry, role):
    allowed_tags = ROLE_TAGS[role]
    return [
        tool
        for tool in registry.list_tools(include_sensitive=(role == "admin"))
        if set(tool["tags"]) & allowed_tags
    ]
```

Cette solution reste volontairement simple. En production, les rôles seraient probablement gérés par une politique centralisée.
