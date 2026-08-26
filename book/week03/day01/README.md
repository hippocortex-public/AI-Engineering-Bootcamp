# Semaine 3 — Jour 1 : Architectures multi-agents

## Position dans le bootcamp

La semaine 2 a construit un agent autonome mono-agent. La semaine 3 démarre le passage vers les systèmes multi-agents.

Le jour 1 pose les architectures fondamentales :

- manager-worker ;
- handoff ;
- router / triage ;
- exécution parallèle ;
- reviewer / critique ;
- état partagé contrôlé ;
- traces d’exécution.

L’objectif n’est pas encore de construire un serveur MCP. Cela arrive plus tard dans la semaine. Aujourd’hui, on apprend à décider quand une architecture multi-agents est justifiée.

## Objectif de la journée

À la fin de cette journée, l’apprenant sait concevoir une architecture multi-agents simple, justifier ses choix, identifier les risques et implémenter une simulation exécutable sans dépendance externe.

## Livrables

```text
book/week03/day01/
├── README.md
├── learning_objectives.md
├── chapter.md
├── exercises.md
├── interview.md
├── challenge.md
├── references.md
├── corriges/
├── diagrams/
├── assets/
└── labs/
```

## Lab

Le lab implémente un simulateur déterministe :

- définition d’agents spécialisés ;
- routage de tâches ;
- orchestration manager-worker ;
- handoff ;
- reviewer ;
- exécution parallèle ;
- traces testables ;
- extension avec un nouvel agent.
