# Corrigé — Exercices

## Exercice 1 — Identifier les composants

Scénario :

```text
Peux-tu vérifier la disponibilité du produit SKU-42 ?
```

Réponse possible :

| Élément | Réponse |
|---|---|
| Entrée utilisateur | `Peux-tu vérifier la disponibilité du produit SKU-42 ?` |
| Intention probable | Vérifier un stock produit |
| Outil nécessaire | `lookup_inventory` |
| Observation attendue | Disponibilité, quantité, SKU |
| Réponse finale possible | `Le produit SKU-42 est disponible. Quantité disponible : 12.` |

## Exercice 2 — Compléter une politique de décision

```python
def decide_action(user_input: str) -> str:
    text = user_input.lower()

    if "commande" in text:
        return "lookup_order"

    if "produit" in text or "stock" in text:
        return "lookup_inventory"

    return "answer_directly"
```

Une variante plus robuste peut aussi détecter `sku-` :

```python
def decide_action(user_input: str) -> str:
    text = user_input.lower()

    if "commande" in text:
        return "lookup_order"

    if "produit" in text or "stock" in text or "sku-" in text:
        return "lookup_inventory"

    return "answer_directly"
```

## Exercice 3 — Ajouter un outil simulé

```python
def lookup_inventory(sku: str) -> dict:
    return {
        "sku": sku,
        "available": True,
        "quantity": 12,
    }
```

## Exercice 4 — Ajouter une trace

Exemple d’intégration :

```python
state.trace.append("received_user_input")

state.action = decide_action(user_input)
state.trace.append(f"selected_action:{state.action}")

if state.action == "lookup_inventory":
    state.observation = lookup_inventory("SKU-42")
    state.trace.append("called_tool:lookup_inventory")

state.trace.append("generated_final_answer")
```

## Exercice 5 — Tester mentalement l’agent

| Entrée | Action attendue |
|---|---|
| `Où est ma commande 123 ?` | `lookup_order` |
| `Le produit SKU-42 est-il disponible ?` | `lookup_inventory` |
| `Bonjour` | `answer_directly` |

## Exercice 6 — Question de conception

Mélanger l’analyse d’intention, l’appel d’outil, la génération de réponse et la gestion d’état rend l’agent difficile à :

- tester ;
- déboguer ;
- faire évoluer ;
- observer ;
- sécuriser.

Une architecture agentique fiable sépare les responsabilités pour que chaque composant puisse être validé indépendamment.
