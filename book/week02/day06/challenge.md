# Challenge — Jour 6

## Objectif

Construire un agent de support capable de résoudre une demande client simple en plusieurs étapes.

L'agent doit utiliser une boucle :

```text
plan -> act -> observe -> update state -> decide
```

## Scénario

L'utilisateur envoie :

```text
Bonjour, ma commande A-100 est en retard. Pouvez-vous m'aider ?
```

L'agent doit :

1. détecter l'identifiant de commande ;
2. consulter un outil simulé `lookup_order`;
3. observer le statut et la date estimée ;
4. rédiger une réponse support ;
5. terminer proprement.

## Contraintes

L'agent doit :

- utiliser un état explicite ;
- ne pas dépasser cinq itérations ;
- journaliser chaque action ;
- refuser les outils inconnus ;
- terminer avec un statut contrôlé ;
- produire une réponse finale seulement si les données nécessaires sont présentes.

## Variante avancée

Ajouter le scénario suivant :

```text
Bonjour, ma commande est en retard.
```

Dans ce cas, l'agent doit :

- ne pas inventer d'identifiant ;
- demander une clarification ;
- terminer avec le statut `waiting_for_user`.

## Critères de réussite

Le challenge est réussi si :

- les tests passent ;
- l'état final est explicite ;
- la réponse finale contient le statut de commande ;
- la boucle ne tourne jamais indéfiniment ;
- les traces permettent de comprendre chaque décision.
