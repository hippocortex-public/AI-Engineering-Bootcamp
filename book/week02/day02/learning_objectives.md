# Objectifs pédagogiques — Semaine 2 Jour 2

## Objectifs conceptuels

À la fin de cette journée, l’apprenant doit pouvoir expliquer :

1. pourquoi le function calling est un contrat entre un modèle et une application ;
2. pourquoi un modèle ne doit jamais exécuter directement du code métier ;
3. comment un schéma d’outil réduit l’ambiguïté entre intention utilisateur et action applicative ;
4. le rôle de la validation avant exécution ;
5. la différence entre texte généré, appel d’outil, résultat d’outil et réponse finale ;
6. pourquoi les erreurs d’outils doivent être traitées comme des cas normaux dans une application IA.

## Objectifs pratiques

L’apprenant doit être capable de :

1. écrire un schéma JSON décrivant une fonction appelable ;
2. implémenter un registre d’outils ;
3. valider les arguments reçus avant d’appeler une fonction ;
4. router un appel vers la bonne fonction Python ;
5. journaliser les appels pour faciliter le debug ;
6. simuler une boucle agentique simple avec appel d’outil ;
7. écrire des tests unitaires autour du dispatch d’outils.

## Objectifs d’architecture

L’apprenant doit savoir concevoir une séparation claire entre :

- le modèle, qui choisit une intention d’action ;
- l’orchestrateur, qui contrôle la boucle ;
- le registre d’outils, qui expose les capacités disponibles ;
- les fonctions métier, qui accèdent aux données ou systèmes externes ;
- la couche de validation, qui protège l’application.

## Critères de réussite

Une solution est considérée correcte si :

- aucun outil non déclaré ne peut être exécuté ;
- les arguments invalides sont rejetés avant l’exécution ;
- les fonctions métier restent indépendantes du modèle ;
- les résultats d’outils sont représentés sous forme structurée ;
- le comportement est testable sans appel réseau ;
- le code peut être exécuté localement.
