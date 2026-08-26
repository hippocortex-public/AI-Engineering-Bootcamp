# Semaine 3 — Jour 6 — Context Engineering

## Position dans le bootcamp

Cette journée appartient à la **Semaine 3 — Multi-Agent & MCP**.

Après avoir construit :

- des architectures multi-agents ;
- des mécanismes de coordination ;
- un serveur MCP ;
- un client MCP ;
- un store d’état partagé ;

ce jour introduit une compétence centrale d’AI Engineering : **concevoir le contexte transmis au modèle**.

Un système agentique ne devient pas fiable uniquement grâce à de meilleurs prompts. Il devient fiable quand le contexte fourni au modèle est :

- sélectionné ;
- hiérarchisé ;
- filtré ;
- compressé ;
- traçable ;
- aligné avec l’objectif courant ;
- compatible avec les limites de fenêtre de contexte.

## Objectif du jour

Construire un moteur pédagogique de **Context Engineering** capable de transformer un état applicatif, des messages récents, des souvenirs, des ressources MCP et des outils disponibles en un **context pack** minimal, contrôlé et exploitable par un agent.

## Compétence cible

À la fin de la journée, l’apprenant sait expliquer et implémenter la différence entre :

- historique conversationnel ;
- mémoire persistante ;
- état partagé ;
- ressources externes ;
- outils disponibles ;
- contexte réellement injecté au modèle.

## Livrables du jour

```text
book/week03/day06/
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
│   ├── context_engineering_pipeline.mmd
│   └── context_budget_sequence.mmd
├── assets/
│   ├── manifest.json
│   ├── context_policy_schema.json
│   └── example_context_items.json
└── labs/
    ├── README.md
    ├── context_engineering.py
    └── test_context_engineering.py
```

## Fil rouge

On construit un agent support interne. Cet agent reçoit une demande utilisateur, mais ne doit pas envoyer tout ce qu’il sait au modèle.

Il doit sélectionner uniquement :

1. l’instruction système utile ;
2. l’état de tâche courant ;
3. les messages récents pertinents ;
4. les souvenirs utilisateur autorisés ;
5. les ressources documentaires utiles ;
6. les outils disponibles pour l’objectif.

## Lab

Le lab est exécutable en Python standard library.

Il implémente :

- `ContextItem` ;
- `ContextPolicy` ;
- `ContextPack` ;
- `ContextEngineer` ;
- un budget de contexte ;
- une stratégie de priorité ;
- un filtre par visibilité ;
- une déduplication ;
- une réduction de PII ;
- un rendu final pour modèle ;
- des tests unitaires.
