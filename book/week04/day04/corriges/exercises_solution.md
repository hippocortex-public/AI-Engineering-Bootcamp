# Corrigé — Exercices

## Exercice 1

1. "L'utilisateur préfère les réponses en tableau." → `preference`
2. "Le paiement a échoué avec le code 402." → `tool_observation`
3. "La tâche courante attend une validation humaine." → `task_state`
4. "Ne jamais appeler l'outil delete sans confirmation." → `policy`
5. "User: peux-tu continuer ?" → `conversation`
6. "Le projet utilise un mini-framework maison." → `fact`

## Exercice 2

```json
{
  "namespace": "user:42",
  "owner_agent": "planner",
  "kind": "preference",
  "content": "L'utilisateur préfère recevoir les explications sous forme d'étapes numérotées.",
  "visibility": "private",
  "tags": ["preference", "format", "steps"],
  "importance": 0.9
}
```

## Exercice 3

L'agent non propriétaire peut recevoir :

```json
[
  {"content": "Fait partagé", "visibility": "shared"},
  {"content": "Annonce publique", "visibility": "public"}
]
```

La mémoire privée ne doit pas être injectée.

## Exercice 4

Un `task_state` est souvent temporaire : formulaire en cours, étape d'un workflow, validation attendue. Un TTL évite de reprendre un état périmé.

Une préférence utilisateur peut rester valable longtemps, mais elle doit quand même pouvoir être modifiée ou supprimée.

## Exercice 5

Exemple :

```text
score = importance
      + 2.0 * lexical_overlap_ratio
      + 1.2 * number_of_matching_tags
```

Chaque résultat doit aussi retourner des raisons : importance, mots communs, tags communs.

## Exercice 6

`forget_namespace("user:42")` doit supprimer toutes les mémoires de ce namespace, sans supprimer les autres namespaces. L'opération doit être auditée.

## Exercice 7

Tests indispensables :

1. isolation par namespace ;
2. respect de la visibilité ;
3. exclusion des records expirés ;
4. redaction PII ;
5. snapshot/restore ;
6. oubli namespace ;
7. scoring/ranking ;
8. audit log.
