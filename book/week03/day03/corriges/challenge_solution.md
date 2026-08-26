# Corrigé — Challenge MCP Server

## Approche de référence

Une solution robuste doit séparer :

- déclaration des capabilities ;
- validation ;
- exécution ;
- formatage ;
- traçage.

Le lab fourni implémente cette séparation.

## Exemple de scénario complet

```python
server = build_demo_server()

server.handle({
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/list"
})

server.handle({
    "jsonrpc": "2.0",
    "id": "2",
    "method": "tools/call",
    "params": {
        "name": "lookup_order",
        "arguments": {"order_id": "ORD-1001"}
    }
})

server.handle({
    "jsonrpc": "2.0",
    "id": "3",
    "method": "resources/read",
    "params": {"uri": "kb://support/refunds"}
})

server.handle({
    "jsonrpc": "2.0",
    "id": "4",
    "method": "tools/call",
    "params": {
        "name": "refund_order",
        "arguments": {
            "order_id": "ORD-1001",
            "amount": 20.0,
            "reason": "late delivery",
            "approved_by_human": False
        }
    }
})
```

Le dernier appel doit échouer avec une erreur contrôlée.

## Implémentation attendue

Le serveur doit avoir :

- un registre de tools ;
- un registre de resources ;
- un registre de prompts ;
- une validation stricte ;
- des erreurs JSON-RPC ;
- des traces.

## Tests indispensables

1. `tools/list` retourne les tools attendus.
2. `lookup_order` retourne une commande connue.
3. `lookup_order` refuse un `order_id` manquant.
4. `resources/read` retourne la policy de remboursement.
5. `prompts/get` retourne le template demandé.
6. `refund_order` refuse sans approbation humaine.
7. `refund_order` accepte avec approbation humaine.
8. Chaque appel ajoute une trace.

## Bonus

Le champ `risk_level` peut être ajouté directement dans la définition du tool.

Exemple :

```python
ToolDefinition(
    name="refund_order",
    description="Refund a customer order after approval.",
    input_schema={...},
    handler=refund_order,
    risk_level="sensitive"
)
```

Puis exposé dans `tools/list`.
