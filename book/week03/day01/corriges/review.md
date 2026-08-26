# Review formateur — Jour 1 Semaine 3

## Intention pédagogique

Cette journée marque le passage de l’agent autonome vers une architecture composée. Le message central : le multi-agent est un compromis d’architecture, pas une amélioration automatique.

## Messages clés

1. Un système multi-agents doit être justifié.
2. Chaque agent doit avoir un rôle clair.
3. Les contrats sont plus importants que les prompts.
4. Le routage est critique.
5. L’état partagé doit rester minimal.
6. Les traces sont indispensables.
7. On peut tester sans LLM réel.

## Points d’attention

Surveiller les conceptions où :

- tous les agents peuvent tout faire ;
- le reviewer réécrit tout ;
- les données sensibles sont partagées partout ;
- aucun statut terminal n’existe ;
- aucune règle anti-boucle n’est prévue ;
- le router ne produit pas de sortie structurée.

## Débrief du lab

Le lab est déterministe volontairement. L’objectif est de rendre testables les décisions d’architecture : routage, handoff, reviewer, traces et extension.

## Transition vers le jour 2

Le jour 2 traitera la coordination : enchaîner les agents, gérer contradictions, séquencement, synchronisation et stratégies de consolidation.
