# Corrigé — Exercices Function Calling

## Exercice 1 — Identifier les responsabilités

| Action | Responsable | Explication |
|---|---|---|
| Choisir `get_order_status` | Modèle | Le modèle interprète l’intention utilisateur. |
| Vérifier que `order_id` est présent | Application | La validation appartient au système contrôlé. |
| Lire la commande en base | Outil métier | L’outil encapsule l’accès aux données. |
| Refuser un argument supplémentaire | Application | Le registre applique le contrat. |
| Transformer le résultat en réponse utilisateur | Modèle ou couche réponse | Le modèle peut reformuler un résultat validé. |
| Journaliser le temps d’exécution | Application | L’observabilité ne dépend pas du modèle. |

## Exercice 2 — Schéma d’outil

```json
{
  "name": "estimate_delivery_date",
  "description": "Estime la date de livraison d'une commande à partir de l'identifiant de commande, du code postal et du mode d'expédition.",
  "parameters": {
    "type": "object",
    "properties": {
      "order_id": {
        "type": "string",
        "description": "Identifiant de commande, par exemple ORD-1001."
      },
      "postal_code": {
        "type": "string",
        "description": "Code postal de destination."
      },
      "shipping_method": {
        "type": "string",
        "enum": ["standard", "express"],
        "description": "Mode d'expédition demandé."
      }
    },
    "required": ["order_id", "postal_code", "shipping_method"],
    "additionalProperties": false
  }
}
```

## Exercice 3 — Validateur minimal

```python
def validate_tool_call(schema: dict, arguments: dict) -> None:
    parameters = schema["parameters"]
    properties = parameters.get("properties", {})
    required = parameters.get("required", [])

    for field in required:
        if field not in arguments:
            raise ValueError(f"Argument manquant: {field}")

    if parameters.get("additionalProperties") is False:
        extra = set(arguments) - set(properties)
        if extra:
            raise ValueError(f"Arguments non autorisés: {sorted(extra)}")

    for field, value in arguments.items():
        if field not in properties:
            continue

        field_schema = properties[field]
        expected_type = field_schema.get("type")

        if expected_type == "string" and not isinstance(value, str):
            raise TypeError(f"{field} doit être une chaîne")

        if "enum" in field_schema and value not in field_schema["enum"]:
            raise ValueError(f"{field} doit être dans {field_schema['enum']}")
```

## Exercice 4 — Dispatcher un appel

```python
def dispatch_tool_call(name: str, arguments: dict) -> dict:
    if name not in registry:
        return {
            "ok": False,
            "error": {
                "code": "UNKNOWN_TOOL",
                "message": f"Outil inconnu: {name}"
            }
        }

    try:
        payload = registry[name](**arguments)
        return {"ok": True, "data": payload}
    except Exception as exc:
        return {
            "ok": False,
            "error": {
                "code": "TOOL_EXECUTION_ERROR",
                "message": str(exc)
            }
        }
```

Dans une solution de production, la validation doit être faite avant l’appel.

## Exercice 5 — Action sensible

`cancel_order` modifie un état métier. Elle peut avoir des conséquences financières, logistiques et utilisateur.

Elle ne doit donc pas être exécutée uniquement parce que le modèle l’a proposée.

Protocole recommandé :

1. le modèle demande l’outil `prepare_cancel_order` ou `request_cancel_confirmation` ;
2. l’application affiche une confirmation explicite à l’utilisateur ;
3. l’utilisateur confirme ;
4. l’application exécute `cancel_order` avec des arguments validés ;
5. l’appel est journalisé.

## Exercice 6 — Lab

Le lab attendu démontre :

- un appel nominal ;
- une erreur de commande introuvable ;
- un outil inconnu ;
- un argument supplémentaire ;
- une valeur enum invalide.

## Exercice 7 — Extension guidée

Exemple de schéma :

```python
return_policy_schema = {
    "name": "get_return_policy",
    "description": "Retourne la politique de retour applicable à un pays et une catégorie produit.",
    "parameters": {
        "type": "object",
        "properties": {
            "country": {"type": "string"},
            "product_category": {"type": "string"}
        },
        "required": ["country", "product_category"],
        "additionalProperties": False
    }
}
```

Exemple d’implémentation :

```python
def get_return_policy(country: str, product_category: str) -> dict:
    if country.upper() == "FR":
        return {"country": country, "product_category": product_category, "return_window_days": 30}
    return {"country": country, "product_category": product_category, "return_window_days": 14}
```
