# Challenge — Jour 6

## Objectif

Construire une mini-couche d'orchestration capable de traiter une demande support avec deux modes :

1. classification structurée ;
2. appel d'outil pour enrichir la réponse.

## Contexte

Vous travaillez sur un backend support e-commerce. Les utilisateurs peuvent :

- signaler un problème de facturation ;
- demander le statut d'une commande ;
- signaler un bug technique.

## Travail demandé

Créer un fichier Python `support_orchestrator.py` qui contient :

1. un schéma de classification support ;
2. une fonction `classify_ticket(text: str) -> dict` ;
3. un registre d'outils ;
4. un outil `get_order_status(order_id: str) -> dict` ;
5. une fonction `handle_user_message(text: str) -> dict`.

## Comportement attendu

### Cas 1 : demande de statut commande

Entrée :

```text
Where is my order A100?
```

Sortie attendue :

```json
{
  "type": "tool_result",
  "tool": "get_order_status",
  "result": {
    "order_id": "A100",
    "status": "shipped",
    "eta_days": 2
  }
}
```

### Cas 2 : ticket support

Entrée :

```text
Urgent API bug blocks checkout.
```

Sortie attendue :

```json
{
  "type": "classification",
  "result": {
    "category": "technical",
    "priority": "high",
    "summary": "Urgent API bug blocks checkout."
  }
}
```

## Contraintes

- Aucun appel réseau.
- JSON valide.
- Pas d'outil appelé si aucun `order_id` clair n'est trouvé.
- Tests unitaires pour les deux cas.
- Gestion explicite des erreurs.

## Critères d'évaluation

- Clarté de l'architecture.
- Validation des sorties.
- Séparation entre décision et exécution.
- Tests reproductibles.
- Code simple et lisible.

## Extension facultative

Ajouter un outil `create_support_ticket` mais ne pas le déclencher directement. La fonction doit seulement créer une demande de confirmation.
