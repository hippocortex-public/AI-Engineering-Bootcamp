# Semaine 3 — Jour 4 — MCP Client

## Position dans le bootcamp

- **Semaine** : 3 — Multi-Agent & MCP
- **Jour** : 4 — MCP Client
- **Pré-requis** :
  - Semaine 2 : agent loop, function calling, structured outputs, state et memory.
  - Semaine 3 J1 : architectures multi-agents.
  - Semaine 3 J2 : coordination.
  - Semaine 3 J3 : MCP Server.

## Résumé

Un serveur MCP expose des capacités. Un client MCP les découvre, les valide, les appelle et les transforme en outils utilisables par un agent.

Cette journée apprend à construire un client MCP minimal mais professionnel :

- initialisation d'une session MCP ;
- découverte des tools ;
- validation locale des arguments ;
- appels JSON-RPC `tools/call` ;
- mapping des erreurs serveur ;
- cache contrôlé de la liste d'outils ;
- adaptation des tools MCP en registre d'outils agentique ;
- traces exploitables pour debug et observabilité.

## Objectif de la journée

À la fin de la journée, l'apprenant sait expliquer et implémenter le rôle d'un client MCP dans une architecture AI Engineering.

Le client ne décide pas à la place de l'agent. Il agit comme une couche d'intégration fiable entre :

1. l'orchestrateur agentique ;
2. le protocole MCP ;
3. les serveurs d'outils ;
4. les politiques de validation, sécurité et observabilité.

## Livrables

```text
book/week03/day04/
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

notebooks/week03/
├── S3_J4_mcp_client.ipynb
└── teacher/
    └── S3_J4_mcp_client_teacher.ipynb
```

## Lab

Le lab construit un client MCP pédagogique en Python standard library.

Il couvre :

- transport JSON-RPC simulé en mémoire ;
- `initialize` ;
- `tools/list` ;
- `tools/call` ;
- validation de schéma JSON simplifiée ;
- refus des outils sensibles sans approbation ;
- adaptation des tools MCP en fonctions appelables par un agent ;
- cache invalidable ;
- traces JSON.

## Commandes

```bash
cd book/week03/day04/labs
python -m py_compile mcp_client.py test_mcp_client.py
python test_mcp_client.py
```

## Critères de réussite

La journée est terminée lorsque :

- tous les fichiers Markdown existent ;
- tous les fichiers de correction existent ;
- les diagrammes Mermaid existent ;
- le lab est exécutable ;
- les tests passent ;
- le notebook étudiant existe ;
- le notebook formateur existe ;
- les corrections ne sont présentes que dans le notebook formateur.
