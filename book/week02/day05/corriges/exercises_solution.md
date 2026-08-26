# Corrigé — Exercices

## Exercice 1 — Classer les informations

| Élément | Classification | Justification |
|---|---|---|
| “L’utilisateur vient de demander un remboursement.” | conversation state | C’est l’intention active de la tâche. |
| `order_id` manque | conversation state | C’est un slot manquant. |
| Préférence pour Python | long-term memory | Préférence stable explicitement donnée. |
| Dernier outil en erreur 404 | short-term memory | Utile pour les prochains tours, pas durable. |
| Numéro de carte bancaire | ne pas mémoriser | Donnée sensible à refuser. |
| Appeler l’utilisateur Sam | long-term memory | Nom d’affichage explicitement donné. |
| Statut `waiting_for_user` | conversation state | État courant de la tâche. |
| Frustration dans le message précédent | short-term memory ou ne pas mémoriser | Utile à court terme pour le ton, pas durable. |

## Exercice 2 — Profil mémoire

Exemple :

```json
{
  "user_id": "user_123",
  "display_name": "Sam",
  "preferences": {
    "language": "Python",
    "answer_style": "concise"
  },
  "facts": [
    {
      "key": "main_framework",
      "value": "FastAPI",
      "source": "explicit_user_statement",
      "updated_at": "2026-08-24T14:00:00"
    }
  ],
  "updated_at": "2026-08-24T14:00:00"
}
```

L’historique complet n’est pas stocké dans le profil.

## Exercice 3 — Politique de promotion

| Phrase | Décision | Couche cible | Justification |
|---|---|---|---|
| Je préfère les réponses courtes. | stocker | long-term memory | Préférence explicite et utile. |
| Aujourd’hui je suis très fatigué. | ne pas stocker durablement | short-term memory éventuelle | Information temporaire. |
| Je travaille principalement avec FastAPI. | stocker | long-term memory | Fait stable utile pour personnaliser les exemples. |
| Mon mot de passe est hunter2. | refuser | aucune | Secret. |
| Pour ce ticket, le produit concerné est Billing API. | stocker pour la tâche | conversation state | Donnée liée à la tâche en cours. |
| Tu peux m’appeler Nadia. | stocker | long-term memory | Nom préféré explicite. |

## Exercice 4 — Lecture du code

1. La mémoire courte est limitée dans `ShortTermMemory.add`.
2. Le state est mis à jour dans `_update_state`.
3. L’isolation utilisateur est assurée par `LongTermMemoryStore._profiles[user_id]`.
4. L’oubli est implémenté dans `forget_user`.
5. Les tests n’appellent pas de LLM car ils valident la couche applicative déterministe.

## Exercice 5 — Test d’isolation

Exemple :

```python
def test_user_preferences_are_isolated():
    agent = MemoryAwareSupportAgent()

    agent.receive("alice", "Je préfère les exemples en Python")
    agent.receive("bob", "Je préfère les exemples en TypeScript")

    alice_response = agent.receive("alice", "Aide-moi à créer un ticket")
    bob_response = agent.receive("bob", "Aide-moi à créer un ticket")

    assert "Python" in alice_response
    assert "TypeScript" in bob_response
    assert "TypeScript" not in alice_response
    assert "Python" not in bob_response
```

## Exercice 6 — Contexte minimal

```text
Profil utilisateur:
- Nom préféré: Nadia
- Langage préféré: Python
- Style de réponse: concise

État courant:
- Intention: create_support_ticket
- Produit: Billing API
- Champ manquant: description
- Statut: collecting

Historique récent:
- user: L'API répond 500 depuis ce matin.
- assistant: Quel produit est concerné ?
- user: Billing API.

Instruction:
Demander la description du problème sans redemander le produit.
```

## Exercice 7 — Anti-patterns

1. Stocker tous les messages crée du bruit, du coût et des risques de données sensibles.
2. Une mémoire globale provoque des fuites entre utilisateurs.
3. Le modèle peut promouvoir des informations temporaires ou inférées à tort.
4. Sans suppression, la mémoire n’est pas gouvernable.
5. Réinjecter toute la mémoire augmente le coût et peut polluer la réponse.

## Exercice 8 — Mini-design

Architecture proposée :

```text
User request
→ ShortTermMemory(max_messages=8)
→ StateTracker(intent, slots, missing_slots)
→ MemoryExtractor(structured output)
→ MemoryPolicy
→ UserProfileStore(user_id)
→ ContextBuilder
→ Model call
```

Mémoire longue autorisée :

- stack préférée ;
- niveau d’expertise ;
- format de réponse.

Mémoire refusée :

- secrets ;
- informations sensibles ;
- erreurs temporaires ;
- transcript complet.
