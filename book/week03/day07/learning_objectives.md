# Objectifs pédagogiques — Jour 7 — Projet multi-agent

## Objectifs principaux

À la fin de cette journée, l’apprenant doit savoir :

1. concevoir un projet multi-agent complet ;
2. décomposer une demande utilisateur en tâches distribuables ;
3. choisir les agents nécessaires à l’exécution d’un objectif ;
4. distinguer orchestration, handoff, outil et mémoire ;
5. exposer des capacités via une couche compatible MCP ;
6. maintenir un état partagé sans fuite de contexte privé ;
7. construire un contexte ciblé pour chaque agent ;
8. tracer chaque étape d’exécution ;
9. intégrer une revue qualité avant réponse finale ;
10. expliquer les limites d’un système multi-agent autonome.

## Objectifs d’architecture

L’apprenant doit être capable de justifier :

- pourquoi un agent central coordonne le workflow ;
- pourquoi tous les agents ne reçoivent pas tout le contexte ;
- pourquoi l’état partagé est versionné ;
- pourquoi les outils sensibles nécessitent une approbation ;
- pourquoi un reviewer indépendant est utile ;
- pourquoi le projet doit avoir des critères d’arrêt explicites.

## Objectifs de code

Le lab doit permettre de pratiquer :

- `dataclasses` pour représenter état, tâches, artefacts et événements ;
- validation d’entrée sans dépendance externe ;
- registre d’outils déterministe ;
- simulation d’appels MCP ;
- filtrage de contexte par rôle ;
- orchestration séquentielle contrôlée ;
- export de trace JSON ;
- tests unitaires avec `unittest`.

## Ce que cette journée ne couvre pas

Cette journée ne couvre pas encore :

- le déploiement production ;
- la persistance en base de données ;
- les files de messages distribuées ;
- l’observabilité complète ;
- la gestion de coûts en production ;
- le sandboxing système avancé.

Ces sujets seront approfondis dans les semaines suivantes.
