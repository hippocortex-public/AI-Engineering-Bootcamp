# Corrigé — Exercices

## Exercice 1

| Responsabilité | Composant attendu |
|---|---|
| Choisir qu’un outil peut être utile | Agent ou modèle via le runner |
| Valider que `priority` vaut `low`, `medium` ou `high` | ToolRegistry |
| Créer réellement un ticket dans un système support | Handler métier |
| Vérifier qu’un utilisateur possède le scope `ticket:write` | ToolRegistry |
| Transformer une exception en résultat normalisé | ToolRegistry |
| Construire la réponse finale à l’utilisateur | Agent |

## Exercice 2

```json
{
  "type": "object",
  "properties": {
    "customer_id": {
      "type": "string",
      "description": "Identifiant stable du client"
    },
    "include_orders": {
      "type": "boolean",
      "description": "Inclure ou non les commandes associées",
      "default": false
    }
  },
  "required": ["customer_id"],
  "additionalProperties": false
}
```

## Exercice 3

Exemple d’enregistrement :

```python
def calculate_discount(arguments, context):
    price = arguments["price"]
    percentage = arguments["percentage"]
    return {"discounted_price": price * (1 - percentage / 100)}

registry.register(
    "calculate_discount",
    "Calcule un prix remisé.",
    {
        "type": "object",
        "properties": {
            "price": {"type": "number"},
            "percentage": {"type": "number"}
        },
        "required": ["price", "percentage"],
        "additionalProperties": False
    },
    calculate_discount,
)
```

## Exercice 4

Modification :

```python
registry.register(
    "calculate_discount",
    "Calcule un prix remisé.",
    schema,
    calculate_discount,
    required_scope="pricing:read",
)
```

Résultat attendu :

- sans `pricing:read` : `blocked` ;
- avec `pricing:read` : `completed`.

## Exercice 5

Le modèle ne doit pas appeler directement une fonction métier parce que cela supprime la frontière de contrôle. Sans registre, il devient difficile de valider les arguments, filtrer les outils, vérifier les permissions, bloquer les actions sensibles, tracer les appels et transformer les erreurs en résultats exploitables.
