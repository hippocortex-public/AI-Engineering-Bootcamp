# Exercices — Architecture d’un agent

## Exercice 1 — Identifier les composants

Lis le scénario suivant :

> Un utilisateur demande : “Peux-tu vérifier la disponibilité du produit SKU-42 ?”

Identifie :

1. l’entrée utilisateur ;
2. l’intention probable ;
3. l’outil nécessaire ;
4. l’observation attendue ;
5. la réponse finale possible.

## Exercice 2 — Compléter une politique de décision

Complète la fonction suivante :

```python
def decide_action(user_input: str) -> str:
    text = user_input.lower()

    if "commande" in text:
        return "lookup_order"

    # TODO: si la demande parle de produit ou de stock,
    # retourner "lookup_inventory"

    return "answer_directly"
```

La fonction doit retourner :

- `lookup_order` pour une demande de commande ;
- `lookup_inventory` pour une demande de stock ou produit ;
- `answer_directly` sinon.

## Exercice 3 — Ajouter un outil simulé

Implémente un outil `lookup_inventory(sku: str)` qui retourne :

```python
{
    "sku": sku,
    "available": True,
    "quantity": 12
}
```

## Exercice 4 — Ajouter une trace

Modifie l’agent pour ajouter les événements suivants dans `state.trace` :

- `received_user_input`
- `selected_action:<action>`
- `called_tool:<tool_name>`
- `generated_final_answer`

## Exercice 5 — Tester mentalement l’agent

Pour chaque entrée, indique l’action attendue :

```text
1. Où est ma commande 123 ?
2. Le produit SKU-42 est-il disponible ?
3. Bonjour
```

## Exercice 6 — Question de conception

Explique pourquoi il est dangereux de mélanger dans une seule fonction :

- l’analyse de l’intention ;
- l’appel d’outil ;
- la génération de réponse ;
- la gestion de l’état.
