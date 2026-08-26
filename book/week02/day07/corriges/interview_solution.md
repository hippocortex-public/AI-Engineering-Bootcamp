# Corrigé — Questions d'entretien

## Question 1

Un assistant outillé peut appeler des fonctions, mais il ne possède pas nécessairement une boucle explicite de planification, observation et décision.

Un agent autonome poursuit un objectif sur plusieurs étapes. Il maintient un état, exécute un plan, observe les résultats et décide s'il doit continuer, s'arrêter ou demander de l'aide.

## Question 2

Sans condition d'arrêt, un agent peut entrer dans une boucle infinie, consommer trop de budget, répéter des appels d'outils ou produire des effets non souhaités.

Les conditions minimales sont :

- objectif atteint ;
- entrée manquante ;
- erreur bloquante ;
- budget dépassé ;
- nombre maximal d'étapes atteint.

## Question 3

On marque les outils sensibles et on impose une validation humaine avant exécution.

Le contrôle doit être côté orchestrateur, pas seulement dans le prompt.

## Question 4

Tester sans LLM réel permet de valider l'architecture déterministe :

- statuts ;
- transitions ;
- garde-fous ;
- sérialisation ;
- registre d'outils ;
- erreurs.

Cela réduit le coût et rend les tests reproductibles.

## Question 5

L'état d'exécution décrit le run en cours.

L'historique de conversation contient les messages récents.

La mémoire longue contient des informations persistantes pouvant survivre aux conversations.

Ces trois couches ne doivent pas être mélangées.

## Question 6

Une trace utile contient :

- l'étape ;
- le type d'événement ;
- le message ;
- l'outil appelé ;
- les arguments importants ;
- l'observation ;
- la raison d'arrêt éventuelle.

## Question 7

Il faut rendre explicites :

- les responsabilités ;
- les outils ;
- les entrées/sorties ;
- les traces ;
- le statut d'exécution.

Ensuite, certaines responsabilités peuvent être extraites vers des agents spécialisés.

## Question 8

Un plan généré dynamiquement peut :

- inventer un outil ;
- ignorer une règle métier ;
- oublier une condition d'arrêt ;
- exécuter une action sensible ;
- produire des étapes impossibles.

Le plan doit donc être validé.

## Question 9

L'agent doit passer en statut `needs_input`, lister les champs manquants et éviter d'appeler des outils qui nécessitent ces champs.

## Question 10

La sérialisation est importante pour :

- reprendre une exécution ;
- auditer les décisions ;
- stocker l'état ;
- gérer les validations humaines ;
- déboguer ;
- reproduire un incident.
