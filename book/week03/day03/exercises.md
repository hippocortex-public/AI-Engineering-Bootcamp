# Exercices — MCP Server

## Exercice 1 — Identifier les capacités serveur

Classez les éléments suivants en `tool`, `resource` ou `prompt`.

1. `lookup_order`
2. `support_policy_refunds`
3. `triage_customer_message_template`
4. `refund_order`
5. `product_catalog_readonly`
6. `create_support_draft`

Livrable attendu : un tableau avec la catégorie et la justification.

## Exercice 2 — Concevoir un tool schema

Concevez le schéma d’entrée du tool `create_support_draft`.

Contraintes :

- `customer_message` est obligatoire ;
- `tone` est obligatoire et vaut `professional`, `friendly` ou `concise` ;
- `language` est obligatoire et vaut `fr` ou `en` ;
- aucune propriété supplémentaire n’est autorisée.

Livrable attendu : un JSON Schema.

## Exercice 3 — Analyser une erreur

On reçoit la requête suivante :

```json
{
  "jsonrpc": "2.0",
  "id": "req-9",
  "method": "tools/call",
  "params": {
    "name": "lookup_order",
    "arguments": {}
  }
}
```

Expliquez :

1. pourquoi elle doit être refusée ;
2. quel code d’erreur JSON-RPC est approprié ;
3. quelle information doit apparaître dans `error.data`.

## Exercice 4 — Sécurité d’un tool sensible

Le tool `refund_order` permet de rembourser une commande.

Proposez trois garde-fous côté serveur.

Livrable attendu : une liste argumentée.

## Exercice 5 — Ajouter une resource

Dans le lab, ajoutez une resource `kb://support/escalation`.

Elle doit retourner une procédure courte expliquant quand escalader un ticket.

Livrable attendu :

- modification du registre de resources ;
- test unitaire vérifiant `resources/read`.

## Exercice 6 — Ajouter une trace

Ajoutez au serveur une trace contenant :

- `request_id` ;
- `method` ;
- `status` ;
- `tool_name` si applicable ;
- `error_code` si applicable.

Livrable attendu : un test qui vérifie qu’un appel invalide est tracé.

## Exercice 7 — Discussion

Expliquez pourquoi un serveur MCP est préférable à un accès direct du modèle aux fonctions Python internes.

Répondez en 10 à 15 lignes.
