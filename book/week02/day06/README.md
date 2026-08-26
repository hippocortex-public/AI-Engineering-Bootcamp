# Semaine 2 — Jour 6 — Agent Loop & planification

## Position dans le bootcamp

Ce jour appartient à la Semaine 2, consacrée au développement d'agents IA.

Après avoir étudié :

- l'architecture générale d'un agent ;
- le function calling ;
- les Structured Outputs ;
- le conversation state ;
- les différentes couches de mémoire ;

ce jour introduit la mécanique centrale qui transforme un simple appel LLM en agent : **la boucle agentique**.

## Thème du jour

**Agent Loop & planification**

Un agent n'est pas seulement un modèle qui répond. C'est un système qui :

1. reçoit un objectif ;
2. analyse l'état courant ;
3. produit un plan ;
4. choisit une action ;
5. exécute éventuellement un outil ;
6. observe le résultat ;
7. met à jour l'état ;
8. décide de continuer, de replanifier ou de terminer.

## Objectif engineering

À la fin de la journée, l'apprenant doit savoir concevoir une boucle agentique déterministe, traçable et testable.

Le but n'est pas de cacher toute la logique dans un prompt. Le but est de construire une orchestration explicite autour du modèle.

## Livrables de la journée

```text
book/week02/day06/
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

Deux notebooks sont également générés :

```text
notebooks/week02/S2_J6_agent_loop_planification.ipynb
notebooks/week02/teacher/S2_J6_agent_loop_planification_teacher.ipynb
```

## Compétence cible

Savoir implémenter une boucle agentique de type :

```text
plan -> act -> observe -> update state -> decide
```

avec :

- une limite d'itérations ;
- un journal d'exécution ;
- une séparation entre plan, action, observation et état ;
- une logique de replanification ;
- une condition d'arrêt claire.

## Résultat attendu

L'apprenant construit un mini-agent capable de résoudre une demande simple à plusieurs étapes en s'appuyant sur des outils simulés et sur un état explicite.
