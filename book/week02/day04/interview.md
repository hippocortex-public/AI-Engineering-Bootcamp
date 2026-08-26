# Questions d’entretien — Conversation State

## Question 1

Explique la différence entre conversation history, conversation state et memory.

## Question 2

Pourquoi un agent multi-tours ne doit-il pas uniquement compter sur le prompt pour se souvenir du contexte ?

## Question 3

Tu construis un agent de remboursement. L’utilisateur donne seulement : `Je veux un remboursement`.

Quel doit être l’état après ce premier tour ?

## Question 4

Comment éviter qu’un agent mélange les informations de deux utilisateurs différents ?

## Question 5

Quels champs mettrais-tu dans un `ConversationState` minimal ?

## Question 6

À quel moment un agent peut-il appeler un outil métier ?

## Question 7

Comment gérer une correction utilisateur ?

Exemple :

```text
Utilisateur : Ma commande est ORD-1001.
Utilisateur : Non, pardon, c’est ORD-2002.
```

## Question 8

Quelle est la différence entre un champ manquant et une valeur invalide ?

## Question 9

Pourquoi faut-il tester explicitement les cas multi-sessions ?

## Question 10

Quels risques de sécurité ou de confidentialité sont liés au Conversation State ?
