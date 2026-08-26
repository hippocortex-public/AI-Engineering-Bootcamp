# Semaine 3 — Jour 2 — Coordination multi-agents

## Position dans le bootcamp

La semaine 3 introduit les systèmes multi-agents et MCP.  
Le jour 1 a défini les architectures multi-agents : manager-worker, handoff, router, reviewer et exécution parallèle.  
Le jour 2 se concentre sur la **coordination** : comment décider quel agent travaille, dans quel ordre, avec quel contexte, quelles règles de validation et quels mécanismes de résolution de conflit.

## Problème traité

Un système multi-agent n'est pas seulement un ensemble d'agents.  
Sans coordination explicite, il devient rapidement :

- non déterministe ;
- coûteux ;
- difficile à déboguer ;
- vulnérable aux boucles infinies ;
- incapable d'expliquer pourquoi une décision a été prise.

La coordination est la couche qui transforme plusieurs capacités isolées en workflow fiable.

## Objectif du jour

À la fin de cette journée, l'apprenant doit savoir construire un coordinateur multi-agent minimal capable de :

1. router une tâche vers les bons agents ;
2. construire un plan d'exécution ;
3. transmettre un contexte limité et utile ;
4. agréger plusieurs réponses ;
5. détecter les désaccords ;
6. décider si une synthèse est suffisante ou si une revue supplémentaire est nécessaire ;
7. produire une trace exploitable.

## Livrables produits

```text
book/week03/day02/
├── README.md
├── learning_objectives.md
├── chapter.md
├── exercises.md
├── interview.md
├── challenge.md
├── references.md
├── corriges/
│   ├── exercises_solution.md
│   ├── interview_solution.md
│   ├── challenge_solution.md
│   └── review.md
├── diagrams/
│   ├── coordination_control_flow.mmd
│   └── disagreement_resolution_sequence.mmd
├── assets/
│   ├── manifest.json
│   ├── coordination_plan_schema.json
│   └── example_coordination_tasks.json
└── labs/
    ├── README.md
    ├── multi_agent_coordinator.py
    └── test_multi_agent_coordinator.py

notebooks/week03/
├── S3_J2_coordination.ipynb
└── teacher/
    └── S3_J2_coordination_teacher.ipynb
```

## Fil rouge

Le lab implémente un coordinateur déterministe pour un assistant IA mono-projet.  
L'utilisateur demande une analyse. Le coordinateur identifie les domaines nécessaires, assigne des agents spécialistes, collecte les résultats, fait intervenir un reviewer si nécessaire, puis génère une décision structurée.

## Compétence AI Engineering

La compétence clé n'est pas de créer beaucoup d'agents.  
La compétence clé est de créer une orchestration explicable, limitée, testable et observable.
