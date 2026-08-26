# Semaine 2 — Jour 7 : Agent autonome

## Position dans le bootcamp

Cette journée conclut la semaine **AI Agent Development**.

Elle assemble les notions construites les jours précédents :

- architecture d'un agent ;
- function calling ;
- structured outputs ;
- conversation state ;
- memory courte, longue et state ;
- agent loop et planification.

L'objectif n'est pas de construire un agent « magique », mais un **agent autonome contrôlé**, capable de poursuivre un objectif, d'utiliser des outils, de conserver son état, de tracer ses décisions et de s'arrêter correctement.

## Problème professionnel

Un assistant IA mono-agent doit traiter une demande utilisateur de support client.

Il doit :

1. comprendre l'objectif ;
2. décider si l'objectif est suffisamment précis ;
3. construire un plan ;
4. exécuter des actions via des outils ;
5. observer les résultats ;
6. mettre à jour son état ;
7. demander validation humaine pour les actions sensibles ;
8. produire une réponse finale fiable.

## Livrables du jour

À la fin de cette journée, l'apprenant doit être capable de livrer un assistant mono-agent avec :

- une boucle d'exécution contrôlée ;
- un registre d'outils ;
- un état sérialisable ;
- une stratégie d'arrêt ;
- des garde-fous simples ;
- des traces exploitables ;
- des tests automatisés.

## Lab principal

Le lab `labs/autonomous_agent.py` implémente un agent autonome de support client.

Il est volontairement exécutable sans API externe afin de tester l'architecture avant d'ajouter un vrai modèle.

## Commandes

```bash
cd book/week02/day07/labs
python autonomous_agent.py
python test_autonomous_agent.py
```

## Critère de réussite

Le jour est validé lorsque :

- le lab s'exécute ;
- les tests passent ;
- l'agent sait s'arrêter ;
- l'agent ne déclenche pas d'action sensible sans approbation ;
- l'état peut être sérialisé ;
- les traces permettent de comprendre les décisions.
