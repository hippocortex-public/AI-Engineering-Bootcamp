# Exercices — Function Calling

## Exercice 1 — Identifier les responsabilités

Pour chaque action, indiquez si elle appartient au modèle, à l’application ou à l’outil métier.

1. Choisir `get_order_status` pour répondre à une question sur une commande.
2. Vérifier que `order_id` est présent.
3. Lire la commande dans une base de données.
4. Refuser un argument supplémentaire non déclaré.
5. Transformer le résultat technique en réponse utilisateur.
6. Journaliser le temps d’exécution de l’outil.

## Exercice 2 — Écrire un schéma d’outil

Écrivez le schéma JSON de l’outil suivant :

Nom : `estimate_delivery_date`

Description : estime la date de livraison d’une commande.

Arguments :

- `order_id`, chaîne obligatoire ;
- `postal_code`, chaîne obligatoire ;
- `shipping_method`, chaîne obligatoire, valeurs possibles : `standard`, `express`.

Contraintes :

- aucun argument supplémentaire n’est autorisé ;
- le schéma doit être suffisamment clair pour un modèle.

## Exercice 3 — Implémenter un validateur minimal

Complétez la fonction suivante.

```python
def validate_tool_call(schema: dict, arguments: dict) -> None:
    """
    Lève une exception si les arguments ne respectent pas le schéma.
    Le schéma supporte seulement:
    - type object;
    - properties;
    - required;
    - additionalProperties;
    - type string;
    - enum.
    """
    ...
```

Cas à gérer :

1. argument obligatoire manquant ;
2. argument non déclaré ;
3. type non string ;
4. valeur hors enum.

## Exercice 4 — Dispatcher un appel

À partir de ce registre :

```python
registry = {
    "get_order_status": get_order_status,
    "estimate_refund": estimate_refund,
}
```

Écrivez une fonction :

```python
def dispatch_tool_call(name: str, arguments: dict) -> dict:
    ...
```

Contraintes :

- refuser les outils inconnus ;
- appeler uniquement les fonctions présentes dans `registry` ;
- retourner un dictionnaire structuré.

## Exercice 5 — Protéger une action sensible

On ajoute l’outil suivant :

```text
cancel_order(order_id: str)
```

Expliquez pourquoi cet outil ne doit pas être exécuté immédiatement après un simple appel du modèle.

Proposez un protocole en deux étapes pour éviter une annulation accidentelle.

## Exercice 6 — Lire et exécuter le lab

Ouvrez le fichier :

```text
book/week02/day02/labs/function_calling_agent.py
```

Puis exécutez :

```bash
python book/week02/day02/labs/function_calling_agent.py
```

Observez :

- les appels d’outils sélectionnés ;
- les résultats structurés ;
- les erreurs contrôlées.

Ensuite, exécutez les tests :

```bash
python book/week02/day02/labs/test_function_calling_agent.py
```

## Exercice 7 — Extension guidée

Ajoutez un outil `get_return_policy`.

Arguments :

- `country`, chaîne obligatoire ;
- `product_category`, chaîne obligatoire.

Le résultat doit indiquer une fenêtre de retour en jours.

Critères :

- l’outil est déclaré dans le registre ;
- les arguments sont validés ;
- un cas de test couvre l’outil ;
- aucun accès dynamique à `globals()` n’est utilisé.
