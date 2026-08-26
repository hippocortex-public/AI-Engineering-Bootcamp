# Semaine 4 — Jour 1 — Architecture d'un mini-framework d'agents

## Position dans le bootcamp

La semaine 4 démarre la construction progressive d'un mini-framework d'agents IA. Après les semaines 2 et 3, l'apprenant sait déjà concevoir un agent, gérer un état conversationnel, orchestrer plusieurs agents et utiliser MCP comme frontière d'outillage. Le jour 1 transforme ces acquis en architecture logicielle maintenable.

## Objectif du jour

Concevoir l'architecture initiale d'un framework minimal d'agents IA capable d'évoluer sur les jours suivants sans devenir un script monolithique.

Le framework doit séparer clairement :

- la définition d'un agent ;
- l'exécution d'une boucle agentique ;
- l'appel au modèle ;
- le registre d'outils ;
- la mémoire ;
- le workflow ;
- l'observabilité ;
- les garde-fous.

## Livrables pédagogiques

À la fin de la journée, l'apprenant dispose :

- d'un modèle d'architecture pour un mini-framework d'agents ;
- d'un vocabulaire clair sur les composants du framework ;
- d'un premier module Python exécutable ;
- d'un ensemble de tests qui valident les invariants d'architecture ;
- d'un diagramme Mermaid d'architecture ;
- d'un plan d'implémentation pour les jours 2 à 7.

## Pré-requis

- Semaine 2 : agents, function calling, structured outputs, state, memory, loop.
- Semaine 3 : coordination multi-agents, MCP server/client, shared state, context engineering.
- Python : dataclasses, typing, JSON, tests sans dépendance externe.

## Résultat attendu

L'apprenant doit être capable d'expliquer pourquoi un framework d'agents ne doit pas commencer par une classe `Agent` énorme, mais par des frontières stables :

```text
AgentDefinition -> Runner -> ModelClient -> ToolRegistry -> MemoryStore -> WorkflowEngine -> Observability
```

Le jour ne construit pas encore tout le framework. Il pose le contrat architectural.
