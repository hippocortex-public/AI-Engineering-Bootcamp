# Corrigés — Jour 6

## Corrigé 1 — Lire une requête moderne

1. Le champ `instructions` décrit le comportement attendu du modèle.
2. Le champ `input` contient le message utilisateur, ici dans un objet avec `role: "user"`.
3. `response_format` indique que la sortie doit respecter une structure exploitable par l'application.
4. Le risque restant est que la sortie soit valide en forme mais incorrecte en contenu. Le schéma ne garantit pas la vérité métier.

## Corrigé 2 — Concevoir un schéma

```json
{
  "type": "object",
  "required": ["topic", "urgency", "employee_message_summary"],
  "properties": {
    "topic": {
      "type": "string",
      "enum": ["payroll", "vacation", "contract", "other"]
    },
    "urgency": {
      "type": "string",
      "enum": ["low", "medium", "high"]
    },
    "employee_message_summary": {
      "type": "string"
    }
  },
  "additionalProperties": false
}
```

## Corrigé 3 — Identifier les bons outils

1. Question générale sur les tokens : Tool Calling généralement inutile. Le modèle peut répondre directement.
2. Statut d'une commande : Tool Calling approprié, car la donnée est externe et dynamique.
3. Résumer un paragraphe fourni : Tool Calling inutile, sauf si le résumé doit être stocké ou enrichi par une source externe.
4. Créer un ticket support : Tool Calling approprié, mais avec validation et confirmation selon le contexte.
5. Inventer une histoire courte : Tool Calling inutile, c'est une génération créative.

## Corrigé 4 — Sécuriser un outil

L'outil `delete_user` est risqué car il produit un effet destructif.

Validations nécessaires :

- authentification ;
- autorisation ;
- existence de l'utilisateur ;
- protection contre la suppression de comptes critiques ;
- confirmation explicite ;
- journalisation ;
- idempotence ;
- éventuellement validation humaine.

Le modèle ne devrait pas pouvoir déclencher directement cet outil dans un flux standard. Une alternative plus sûre est :

```python
def request_user_deletion_review(user_id: str, reason: str) -> dict:
    ...
```

Cette fonction crée une demande de revue plutôt qu'une suppression immédiate.

## Corrigé 5 — Parser un tool call

```python
import json

def parse_tool_call(raw: str) -> dict:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("Tool call must be valid JSON") from exc

    if set(payload.keys()) != {"name", "arguments"}:
        raise ValueError("Tool call must contain exactly name and arguments")
    if not isinstance(payload["name"], str):
        raise ValueError("Tool name must be a string")
    if not isinstance(payload["arguments"], dict):
        raise ValueError("Tool arguments must be an object")
    return payload
```

## Corrigé 6 — Analyse d'architecture

1. Le problème principal est que le modèle semble appeler directement l'API de paiement. Cela mélange raisonnement probabiliste et action métier critique.
2. Architecture proposée :

```text
Utilisateur -> Application -> LLM
LLM -> demande d'outil
Application -> validation métier
Application -> API paiement
Application -> réponse contrôlée
```

3. La validation doit être placée côté application, avant tout appel externe.
4. Les logs doivent couvrir la requête utilisateur, la décision d'appel d'outil, les arguments validés, le résultat de l'outil, les erreurs et l'identifiant de corrélation.
