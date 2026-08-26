# Review formateur — Semaine 2 Jour 5

## Objectif de la review

Valider que l’apprenant comprend la mémoire comme une couche d’architecture et non comme une simple accumulation de messages.

## Points à vérifier

### Compréhension conceptuelle

L’apprenant doit distinguer :

- short-term memory ;
- conversation state ;
- long-term memory ;
- mémoire applicative ;
- historique brut.

### Compréhension technique

L’apprenant doit savoir expliquer :

- pourquoi `ShortTermMemory` limite le nombre de messages ;
- pourquoi `LongTermMemoryStore` est indexé par `user_id` ;
- pourquoi `ConversationState` ne stocke pas les préférences ;
- pourquoi `forget_user` est nécessaire ;
- pourquoi les tests sont déterministes.

### Qualité du code

Vérifier que :

- le code s’exécute sans dépendance externe ;
- les dataclasses sont lisibles ;
- les fonctions ont une responsabilité claire ;
- les tests couvrent l’isolation utilisateur ;
- la sérialisation ne casse pas les données.

## Questions de review

1. Quelle information du lab appartient au state et non à la mémoire longue ?
2. Pourquoi le nom préféré est-il une mémoire longue acceptable ?
3. Que faudrait-il changer avant d’utiliser ce système en production ?
4. Comment ajouter une politique de consentement utilisateur ?
5. Quelle différence entre `forget_user` et `clear_current_state` ?

## Attendus de réponse

L’apprenant doit répondre que :

- les données de ticket appartiennent au state ;
- les préférences explicites peuvent être stockées ;
- les secrets doivent être refusés ;
- l’isolation par utilisateur est obligatoire ;
- l’oubli est une fonctionnalité de gouvernance ;
- la mémoire longue doit rester sélective.

## Checklist de complétion

- [x] README présent
- [x] learning_objectives présent
- [x] chapter présent
- [x] exercises présent
- [x] interview présent
- [x] challenge présent
- [x] references présent
- [x] corrigés présents
- [x] diagrams présents
- [x] assets présents
- [x] labs présents
- [x] notebook étudiant généré
- [x] notebook formateur généré
- [x] code exécutable
- [x] tests automatisés

## Propositions d’amélioration

Ces propositions ne modifient pas les spécifications.

- Ajouter un exemple avec stockage SQLite en Semaine 4.
- Ajouter une démonstration de résumé incrémental en Semaine 8.
- Ajouter un mini-exercice sur consentement et suppression utilisateur.
