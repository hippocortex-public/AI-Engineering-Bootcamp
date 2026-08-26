# Semaine 3 — Jour 7 — Projet multi-agent

## Position dans le bootcamp

Cette journée appartient à la **Semaine 3 — Multi-Agent & MCP**.

Elle clôture la semaine en assemblant les briques construites précédemment :

- architectures multi-agents ;
- coordination ;
- serveur MCP ;
- client MCP ;
- partage d’état ;
- context engineering.

Le jour 7 n’introduit pas une nouvelle famille de concepts. Il transforme les concepts de la semaine en un **projet intégrateur** : un système multi-agent capable de traiter une demande métier, de répartir le travail, d’utiliser des outils exposés sous forme MCP, de partager un état contrôlé et de produire un livrable vérifiable.

## Objectif du jour

Construire un **assistant multi-agent de livraison technique**.

Le système doit être capable de :

1. comprendre un objectif utilisateur ;
2. produire un plan de travail ;
3. distribuer les tâches à plusieurs agents spécialisés ;
4. appeler des outils via une couche compatible MCP ;
5. maintenir un état partagé versionné ;
6. construire un contexte minimal pour chaque agent ;
7. agréger les contributions ;
8. exécuter une revue qualité ;
9. retourner un résultat traçable.

## Compétence cible

À la fin de la journée, l’apprenant sait concevoir un projet multi-agent complet sans confondre :

- agent ;
- outil ;
- serveur MCP ;
- client MCP ;
- état partagé ;
- contexte ;
- trace ;
- artefact final.

## Projet construit

Le lab implémente un orchestrateur pédagogique nommé `DeliveryCoordinator`.

Il utilise :

- un agent `planner` pour découper le travail ;
- un agent `researcher` pour extraire les informations nécessaires ;
- un agent `engineer` pour produire une proposition technique ;
- un agent `security` pour vérifier les actions sensibles ;
- un agent `reviewer` pour contrôler la qualité finale ;
- un `SharedStateStore` pour stocker l’état visible par rôle ;
- un `ContextBuilder` pour générer le contexte transmis à chaque agent ;
- un `MCPToolAdapter` pour exposer des outils sous une interface standardisée ;
- une trace structurée exportable en JSON.

## Résultat attendu

L’apprenant obtient une base exécutable qui simule un projet multi-agent réaliste, sans dépendance externe ni appel API.

Le but n’est pas de masquer la complexité derrière un framework. Le but est de comprendre les responsabilités d’architecture qui existeront aussi dans un framework professionnel.

## Fichiers du jour

```text
book/week03/day07/
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
│   ├── multi_agent_project_architecture.mmd
│   └── multi_agent_delivery_sequence.mmd
├── assets/
│   ├── manifest.json
│   ├── project_scenario.json
│   ├── multi_agent_project_schema.json
│   └── acceptance_criteria.json
└── labs/
    ├── README.md
    ├── multi_agent_project.py
    └── test_multi_agent_project.py
```

## Règle pédagogique

Un projet multi-agent n’est pas fiable parce qu’il contient beaucoup d’agents.

Il devient fiable quand chaque agent a :

- une responsabilité claire ;
- un contexte minimal ;
- un état partagé contrôlé ;
- des outils bornés ;
- des critères d’arrêt ;
- des traces exploitables ;
- une revue finale.
