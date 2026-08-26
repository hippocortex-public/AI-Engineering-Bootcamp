# Corrigés — Questions d’entretien Conversation State

## Question 1

L’historique est la liste des messages.

Le state est la représentation structurée de la situation courante.

La memory est l’information durable qui peut survivre à la conversation.

Formule simple :

```text
History = ce qui a été dit.
State = où en est le workflow.
Memory = ce qu’on conserve durablement.
```

## Question 2

Un prompt n’est pas une source de vérité fiable.

Il peut devenir long, coûteux, ambigu ou incomplet.

Le backend doit conserver les éléments critiques dans une structure explicite, testable et validable.

## Question 3

Après le premier tour :

```json
{
  "intent": "refund",
  "slots": {},
  "missing_fields": ["order_id", "email", "reason"],
  "status": "collecting"
}
```

La réponse assistant doit demander le premier champ manquant, par exemple le numéro de commande.

## Question 4

Il faut isoler l’état par session.

Bonnes pratiques :

- clé de stockage par `session_id` ;
- vérification du `user_id` ;
- pas de variable globale mutable partagée ;
- tests multi-sessions ;
- expiration des sessions ;
- contrôle d’accès au store.

## Question 5

Un state minimal peut contenir :

- `session_id` ;
- `user_id` ;
- `intent` ;
- `slots` ;
- `messages` ;
- `tool_results` ;
- `turn_count` ;
- `status`.

## Question 6

Un agent peut appeler un outil métier quand :

- l’intention est connue ;
- tous les champs requis sont présents ;
- les valeurs sont valides ;
- la session est autorisée ;
- l’action n’a pas déjà été exécutée ou est idempotente.

## Question 7

Une correction utilisateur doit être traitée explicitement.

Le système doit :

- remplacer la valeur ;
- journaliser la correction ;
- invalider les résultats d’outils dépendants de l’ancienne valeur ;
- redemander confirmation si l’action est sensible.

## Question 8

Un champ manquant est absent.

Une valeur invalide est présente mais inutilisable.

Exemple :

```text
missing: email absent
invalid: email = "pas-un-email"
```

Les deux cas ne déclenchent pas forcément la même réponse.

## Question 9

Les tests multi-sessions vérifient qu’un état ne fuit pas d’une conversation à l’autre.

Ils protègent contre :

- les variables globales ;
- les caches mal indexés ;
- les erreurs de session ;
- les bugs de concurrence ;
- les fuites de données personnelles.

## Question 10

Risques principaux :

- fuite de données entre sessions ;
- conservation excessive de données personnelles ;
- stockage de secrets ;
- absence d’expiration ;
- absence de chiffrement ;
- logs trop détaillés ;
- action métier déclenchée avec un état incomplet.
