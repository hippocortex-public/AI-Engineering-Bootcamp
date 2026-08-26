# Objectifs pédagogiques — Jour 2 — Coordination

## Objectifs principaux

À la fin de cette journée, l'apprenant doit pouvoir :

- expliquer pourquoi la coordination est une couche distincte de l'intelligence d'un agent ;
- différencier routing, handoff, délégation, vote, revue et synthèse ;
- concevoir une politique de coordination explicite ;
- limiter le contexte transmis à chaque agent ;
- représenter une exécution multi-agent sous forme de trace ;
- détecter un désaccord entre agents ;
- déclencher une revue ou une clarification ;
- tester un coordinateur sans appeler un LLM réel.

## Objectifs techniques

L'apprenant doit savoir implémenter :

- un registre d'agents spécialistes ;
- une fonction de sélection d'agents à partir d'une tâche ;
- un plan de coordination sérialisable ;
- une boucle d'exécution bornée ;
- une stratégie d'agrégation ;
- une détection simple de conflit ;
- une synthèse finale structurée ;
- des tests unitaires pour valider la stabilité du workflow.

## Objectifs d'architecture

L'apprenant doit être capable de justifier :

- pourquoi le coordinateur ne doit pas tout déléguer aveuglément ;
- pourquoi un agent ne doit recevoir que le contexte nécessaire ;
- pourquoi les handoffs doivent être observables ;
- pourquoi les décisions sensibles doivent passer par une étape de revue ;
- pourquoi la coordination doit être déterministe autant que possible.

## Critères de réussite

Une solution est considérée correcte si elle :

- assigne les tâches aux bons agents ;
- ne sélectionne pas d'agents inutiles ;
- conserve une trace claire ;
- produit un résultat stable pour une même entrée ;
- sait signaler un conflit ;
- déclenche une revue en cas de risque élevé ;
- reste exécutable sans dépendances externes.
