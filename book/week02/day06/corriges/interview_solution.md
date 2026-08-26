# Corrigé — Questions d'entretien — Jour 6

## Réponse 1

Un chatbot simple transforme un message en réponse.

Un agent avec boucle agentique peut planifier, appeler des outils, observer des résultats, mettre à jour un état et décider de continuer ou de terminer.

## Réponse 2

La séparation action/observation rend le système traçable et testable.

L'action décrit ce que l'agent veut faire. L'observation décrit ce qui s'est réellement passé.

## Réponse 3

Une condition d'arrêt est une règle qui indique quand la boucle doit se terminer.

Exemples :

- objectif atteint ;
- réponse finale produite ;
- information utilisateur manquante ;
- erreur non récupérable ;
- limite d'itérations atteinte.

## Réponse 4

On peut éviter les appels répétitifs en combinant :

- limite d'itérations ;
- journal des actions déjà exécutées ;
- détection d'action identique ;
- état mis à jour après chaque observation ;
- politique empêchant un appel sans nouvelle information.

## Réponse 5

La planification initiale produit une stratégie avant l'exécution.

La replanification adapte cette stratégie après une observation, une erreur ou une nouvelle contrainte.

## Réponse 6

Il faut demander une clarification lorsque l'information manquante bloque une action sûre.

Exemple : l'agent ne peut pas appeler `lookup_order` sans identifiant de commande.

## Réponse 7

On peut remplacer le LLM par une policy déterministe ou un simulateur.

Cela permet de tester :

- les transitions d'état ;
- la sélection d'actions ;
- les erreurs ;
- les limites d'itérations ;
- les statuts finaux.

## Réponse 8

Le state représente la connaissance courante de résolution.

Il relie le goal, le plan, les observations, les champs collectés, les actions passées et le statut final.

## Réponse 9

La traçabilité permet de comprendre pourquoi l'agent a agi.

Elle est essentielle pour :

- déboguer ;
- auditer ;
- évaluer ;
- améliorer les prompts ;
- analyser les coûts ;
- sécuriser la production.

## Réponse 10

Le function calling structure les actions possibles.

Les Structured Outputs structurent les décisions, plans et réponses.

Ensemble, ils réduisent l'ambiguïté entre le modèle et l'orchestrateur applicatif.
