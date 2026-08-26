# Exercices

## Exercice 1 — Identifier les responsabilités

Pour chaque responsabilité ci-dessous, indique si elle appartient plutôt à l’agent, au registre d’outils ou au handler métier.

| Responsabilité | Composant attendu |
|---|---|
| Choisir qu’un outil peut être utile | |
| Valider que `priority` vaut `low`, `medium` ou `high` | |
| Créer réellement un ticket dans un système support | |
| Vérifier qu’un utilisateur possède le scope `ticket:write` | |
| Transformer une exception en résultat normalisé | |
| Construire la réponse finale à l’utilisateur | |

## Exercice 2 — Concevoir un schéma

Écris un schéma d’entrée pour un outil `lookup_customer`.

Contraintes :

- `customer_id` est obligatoire ;
- `customer_id` est une chaîne ;
- `include_orders` est un booléen optionnel avec valeur par défaut `false` ;
- aucun champ inattendu n’est autorisé.

## Exercice 3 — Ajouter un outil non sensible

Dans le lab, ajoute un outil `calculate_discount`.

Contraintes :

- arguments : `price` nombre, `percentage` nombre ;
- les deux champs sont obligatoires ;
- l’outil retourne `{"discounted_price": ...}` ;
- l’outil n’est pas sensible.

## Exercice 4 — Ajouter une politique

Modifie l’outil `calculate_discount` pour exiger le scope `pricing:read`.

Teste deux contextes :

1. sans scope ;
2. avec scope.

## Exercice 5 — Raisonnement d’architecture

Explique pourquoi le modèle ne doit jamais appeler directement une fonction Python métier sans passer par un registre.
