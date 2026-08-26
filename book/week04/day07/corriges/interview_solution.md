# Corrigé — Questions d'entretien

## Question 1

L'implémentation de composants isolés vérifie que chaque brique fonctionne séparément. L'intégration vérifie que les contrats entre briques sont compatibles : types, responsabilités, erreurs, traces et ordre d'exécution.

## Question 2

On évite une classe agent trop grosse en séparant :

- la définition de l'agent ;
- l'exécution du workflow ;
- l'appel d'outils ;
- la mémoire ;
- l'observabilité ;
- les garde-fous.

L'agent décrit un rôle. Il ne doit pas devenir toute l'application.

## Question 3

Un registre d'outils centralise la validation, les permissions, les schémas, l'audit et les erreurs. Un appel direct contourne ces contrôles.

## Question 4

La mémoire contient des informations réutilisables entre exécutions. L'état de workflow décrit l'exécution actuelle. L'historique de conversation conserve les messages récents.

Ces trois éléments peuvent se combiner, mais ne doivent pas être confondus.

## Question 5

Une trace utile doit permettre de reconstruire :

- l'entrée ;
- les étapes exécutées ;
- les outils appelés ;
- les décisions ;
- les erreurs ;
- les durées ;
- les actions bloquées.

Elle doit éviter d'exposer les données sensibles.

## Question 6

Le framework doit refuser l'exécution et retourner un statut explicite, par exemple `blocked`. Il doit tracer le blocage et indiquer quelle approbation manque.

## Question 7

Invariants à tester :

- tous les agents référencés existent ;
- tous les outils référencés existent ;
- les dépendances n'ont pas de cycle ;
- les outils sensibles sont protégés ;
- les traces sont générées ;
- les résultats sont sérialisables ;
- les erreurs sont déterministes.

## Question 8

Pour préparer l'asynchrone :

- isoler les handlers d'outils ;
- rendre les appels IO abstraits ;
- éviter l'état global mutable ;
- ajouter des identifiants de run ;
- prévoir une file d'événements ;
- séparer orchestration et transport.
