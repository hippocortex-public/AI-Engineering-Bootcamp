# Exercices — Jour 6

## Exercice 1 — Lire une requête moderne

Considérer la requête suivante :

```json
{
  "model": "example-modern-llm",
  "instructions": "Classify the support ticket. Return only JSON.",
  "input": [
    {
      "role": "user",
      "content": "My payment failed but I was still charged."
    }
  ],
  "response_format": {
    "type": "json_schema"
  }
}
```

Questions :

1. Quel champ décrit le comportement attendu du modèle ?
2. Quel champ contient le message utilisateur ?
3. Pourquoi le champ `response_format` est-il utile ?
4. Quel risque existe encore malgré `response_format` ?

## Exercice 2 — Concevoir un schéma

Créer un schéma JSON pour classer une demande RH avec les champs :

- `topic` : `payroll`, `vacation`, `contract`, `other`
- `urgency` : `low`, `medium`, `high`
- `employee_message_summary` : chaîne de caractères

Contraintes :

- les trois champs sont obligatoires ;
- aucun champ supplémentaire n'est autorisé.

## Exercice 3 — Identifier les bons outils

Pour chaque besoin, dire si le Tool Calling est approprié.

1. Répondre à une question générale : "Qu'est-ce qu'un token ?"
2. Obtenir le statut d'une commande client.
3. Résumer un paragraphe fourni par l'utilisateur.
4. Créer un ticket dans un outil support.
5. Inventer une histoire courte.

Justifier chaque réponse.

## Exercice 4 — Sécuriser un outil

On expose l'outil suivant :

```python
def delete_user(user_id: str) -> dict:
    ...
```

Questions :

1. Pourquoi cet outil est-il risqué ?
2. Quelles validations faut-il ajouter ?
3. Faut-il toujours permettre au modèle de demander cet outil ?
4. Quelle alternative plus sûre peut-on proposer ?

## Exercice 5 — Parser un tool call

Écrire une fonction qui accepte une chaîne JSON et vérifie que l'objet contient exactement :

```json
{
  "name": "...",
  "arguments": {}
}
```

La fonction doit rejeter :

- JSON invalide ;
- champ manquant ;
- champ supplémentaire ;
- `arguments` qui n'est pas un objet.

## Exercice 6 — Analyse d'architecture

Une équipe a construit le flux suivant :

```text
Utilisateur -> LLM -> Appel direct API paiement -> Réponse utilisateur
```

Questions :

1. Quel est le problème principal ?
2. Quelle architecture proposer ?
3. Où placer la validation ?
4. Où placer les logs ?
