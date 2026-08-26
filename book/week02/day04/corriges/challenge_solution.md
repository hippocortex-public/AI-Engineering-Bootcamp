# Corrigé — Challenge Agent de support stateful

## Solution de référence

Le lab fournit une solution complète dans :

```text
book/week02/day04/labs/conversation_state_agent.py
```

L’implémentation contient :

- `ConversationState` ;
- `Message` ;
- `initialize_state` ;
- `handle_user_message` ;
- `missing_required_fields` ;
- `serialize_state` ;
- `restore_state` ;
- `execute_ready_action`.

## Stratégie retenue

La solution utilise une extraction déterministe afin de rendre le lab exécutable sans service externe.

Dans un agent réel, l’extraction pourrait être produite par un modèle avec Structured Outputs.

Le backend garderait néanmoins la même responsabilité :

```text
sortie modèle
→ validation
→ mise à jour du state
→ décision applicative
```

## Exemple de déroulé

```python
state = initialize_state("session_001", "user_123")

state, reply = handle_user_message(state, "Je veux un remboursement.")
assert state.intent == "refund"
assert state.status == "collecting"

state, reply = handle_user_message(state, "ORD-1001")
assert state.slots["order_id"] == "ORD-1001"

state, reply = handle_user_message(state, "lea@example.com")
assert state.slots["email"] == "lea@example.com"

state, reply = handle_user_message(state, "J'ai été facturée deux fois.")
assert state.slots["reason"] == "double_billing"
assert state.status == "ready_for_action"
```

## Points importants

### 1. L’intention est conservée

Lorsque l’utilisateur répond seulement :

```text
ORD-1001
```

le système garde l’intention `refund`.

Il ne repart pas à zéro.

### 2. Les champs manquants sont calculés

La fonction `missing_required_fields` compare :

- les champs requis par intention ;
- les slots déjà présents.

Elle ne dépend pas du texte brut.

### 3. L’action est protégée

`execute_ready_action` refuse d’agir si le state n’est pas `ready_for_action`.

Cela évite les appels outils prématurés.

### 4. Les sessions sont isolées

Chaque state est un objet indépendant.

Les tests vérifient qu’un email ajouté dans une session ne se retrouve pas dans une autre.

### 5. La sérialisation est testée

La solution vérifie qu’un état peut être converti en JSON puis restauré.

## Améliorations possibles hors spécification

### Propositions d'amélioration

- Ajouter une provenance par slot : `user`, `tool`, `model`.
- Ajouter un champ `schema_version`.
- Ajouter une expiration de session.
- Ajouter un store Redis.
- Ajouter une politique de redaction des données sensibles.
- Ajouter un mécanisme d’idempotence pour les actions métier.
