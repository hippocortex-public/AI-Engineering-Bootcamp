# Corrigés — Exercices Conversation State

## Exercice 1 — Identifier le problème de statelessness

Le dernier message seul est :

```text
ORD-1001
```

Ce message indique probablement un numéro de commande, mais il ne suffit pas.

Le système doit connaître l’état précédent :

- l’intention active était `order_status` ;
- le champ collecté est `order_id` ;
- il manque probablement `email` si le workflow l’exige ;
- la prochaine action est de demander l’adresse email ou d’appeler l’outil si tous les champs sont présents.

Sans state, l’assistant ne sait pas si `ORD-1001` concerne un suivi de commande, un remboursement ou une autre demande.

## Exercice 2 — Concevoir un state minimal

Exemple :

```python
@dataclass
class ConversationState:
    session_id: str
    user_id: str
    intent: str
    slots: dict[str, str]
    messages: list[dict[str, str]]
    tool_results: dict[str, dict]
    turn_count: int
    status: str
```

Rôle des champs :

| Champ | Type | Rôle |
|---|---:|---|
| `session_id` | `str` | Identifie une conversation précise. |
| `user_id` | `str` | Relie la session à un utilisateur. |
| `intent` | `str` | Représente le besoin actif. |
| `slots` | `dict[str, str]` | Stocke les champs métier collectés. |
| `messages` | `list[dict]` | Conserve l’historique court. |
| `tool_results` | `dict` | Stocke les observations d’outils. |
| `turn_count` | `int` | Suit le nombre de tours utilisateur. |
| `status` | `str` | Indique la progression du workflow. |

## Exercice 3 — Calculer les champs manquants

Pour `refund`, les champs requis sont :

```python
{"order_id", "email", "reason"}
```

Les slots connus sont :

```python
{"order_id"}
```

Les champs manquants sont donc :

```python
{"email", "reason"}
```

L’assistant doit poser une seule question ciblée, par exemple :

```text
Quelle adresse email est associée à la demande ?
```

Il demandera ensuite la raison du remboursement si l’email est fourni.

## Exercice 4 — Détecter une fuite d’état

Ce bug est grave parce qu’il expose l’email d’Alice dans la session de Bob.

Il viole l’isolation des sessions.

Le test à écrire :

```python
state_a = new_state("A", "alice")
state_b = new_state("B", "bob")

handle_user_message(state_a, "alice@example.com")

assert "email" not in state_b.slots
```

La solution consiste à stocker l’état par clé de session, par exemple :

```text
conversation_state:{session_id}
```

Il faut éviter les variables globales mutables partagées sans isolation.

## Exercice 5 — State ou Memory ?

| Information | Classement | Justification |
|---|---|---|
| Numéro de commande courant | Conversation State | Sert à la tâche en cours. |
| Préférence durable pour le français | Memory | Peut être réutilisée dans plusieurs conversations. |
| Mot de passe envoyé par erreur | Ni l’un ni l’autre | Donnée sensible à ne pas conserver. |
| Statut `ready_for_action` | Conversation State | Décrit la progression courante. |
| Résumé long terme des projets | Memory | Persiste au-delà de la session. |
| Dernier message assistant | Conversation State | Fait partie de l’historique court. |
| Résultat d’un outil courant | Conversation State | Observation liée à cette conversation. |
| Donnée personnelle non nécessaire | Ni l’un ni l’autre | Principe de minimisation. |

## Exercice 6 — Sérialisation

Un état doit pouvoir être sérialisé pour :

- reprendre une conversation après une interruption ;
- changer de worker backend ;
- stocker temporairement la session ;
- auditer un comportement ;
- tester une séquence complète.

Stores possibles :

- Redis ;
- PostgreSQL ;
- SQLite ;
- un store de session managé.

La sérialisation ne suffit pas à garantir la sécurité.

Il faut aussi gérer :

- le chiffrement ;
- la durée de rétention ;
- les droits d’accès ;
- la minimisation des données ;
- la suppression ;
- l’isolation par utilisateur et par session.
