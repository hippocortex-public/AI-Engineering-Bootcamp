# Exercices — Conversation State

## Exercice 1 — Identifier le problème de statelessness

Analyse la conversation suivante :

```text
Utilisateur : Je veux suivre ma commande.
Assistant : Quel est votre numéro de commande ?
Utilisateur : ORD-1001
```

Explique pourquoi le dernier message seul ne suffit pas pour générer une bonne réponse.

Ta réponse doit mentionner :

- l’intention ;
- le champ collecté ;
- les champs potentiellement manquants ;
- la prochaine action.

## Exercice 2 — Concevoir un state minimal

Conçois un objet `ConversationState` pour un agent de support.

Il doit contenir au minimum :

- `session_id` ;
- `user_id` ;
- `intent` ;
- `slots` ;
- `messages` ;
- `tool_results` ;
- `turn_count` ;
- `status`.

Pour chaque champ, explique :

- son rôle ;
- son type probable ;
- pourquoi il est utile au backend.

## Exercice 3 — Calculer les champs manquants

On définit les champs requis suivants :

```python
REQUIRED_FIELDS = {
    "order_status": {"order_id", "email"},
    "refund": {"order_id", "email", "reason"},
    "technical_issue": {"email", "issue_summary"},
}
```

État courant :

```json
{
  "intent": "refund",
  "slots": {
    "order_id": "ORD-1001"
  }
}
```

Quels champs manquent ?

Quelle question l’assistant doit-il poser ensuite ?

## Exercice 4 — Détecter une fuite d’état

Deux conversations existent.

Session A :

```json
{
  "session_id": "A",
  "user_id": "alice",
  "slots": {
    "email": "alice@example.com"
  }
}
```

Session B :

```json
{
  "session_id": "B",
  "user_id": "bob",
  "slots": {}
}
```

Un bug provoque l’utilisation de l’email d’Alice dans la session de Bob.

Explique :

- pourquoi ce bug est grave ;
- quelle règle d’architecture il viole ;
- quel test devrait exister ;
- quelle solution de stockage éviterait ce risque.

## Exercice 5 — State ou Memory ?

Classe les informations suivantes dans `Conversation State`, `Memory` ou `Ni l’un ni l’autre`.

1. Le numéro de commande donné dans la conversation en cours.
2. La préférence durable de l’utilisateur pour des réponses en français.
3. Un mot de passe envoyé par erreur dans le chat.
4. Le statut `ready_for_action`.
5. Le résumé long terme des projets préférés d’un utilisateur.
6. Le dernier message assistant.
7. Le résultat d’un outil appelé dans la conversation actuelle.
8. Une donnée personnelle non nécessaire à la tâche.

## Exercice 6 — Sérialisation

Explique pourquoi un état conversationnel doit pouvoir être sérialisé.

Donne deux exemples de stores possibles.

Explique aussi pourquoi la sérialisation ne suffit pas à garantir la sécurité.
