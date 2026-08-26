# Corrections — Interview

## Réponse 1

Un workflow engine rend explicite le processus métier que l'agent doit suivre. Il apporte un contrat d'exécution, des dépendances, des statuts, des retries, des garde-fous et une trace. Cela améliore la testabilité et l'auditabilité.

## Réponse 2

Une boucle agentique est dynamique : le système observe, décide, agit, puis réévalue. Un workflow déterministe est contractuel : les étapes et dépendances sont définies à l'avance. Les deux peuvent coexister : une étape de workflow peut contenir une boucle agentique limitée.

## Réponse 3

On détecte un cycle avec un tri topologique. Si l'algorithme ne peut pas ordonner toutes les étapes, il reste des dépendances non résolues : le graphe contient un cycle.

## Réponse 4

Un prompt est une consigne, pas une garantie d'exécution. Une action sensible doit être contrôlée par le moteur ou une couche de politique, car cette couche est testable, observable et indépendante du comportement probabiliste du modèle.

## Réponse 5

Une trace utile contient au minimum : identifiant de run, nom du workflow, étape, événement, timestamp, tentative, handler, erreur éventuelle, raison de skip ou de blocage, statut final.

## Réponse 6

Il faut rendre les actions idempotentes, tracer les tentatives, limiter les retries, distinguer erreurs temporaires et erreurs définitives, et éviter de réexécuter une action externe non idempotente sans clé d'idempotence.

## Réponse 7

`failed` signifie erreur technique ou métier non récupérée. `blocked` signifie attente d'une approbation ou d'une politique. `skipped` signifie étape volontairement non exécutée, par condition fausse ou dépendance non satisfaite.

## Réponse 8

Pour aller vers la production, il faut ajouter persistance, reprise après crash, exécution asynchrone, queue, timeouts réels, idempotence, annulation, métriques, versioning, secrets, gestion de droits et observabilité centralisée.
