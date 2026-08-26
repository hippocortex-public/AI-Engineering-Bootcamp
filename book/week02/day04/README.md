# Semaine 2 — Jour 4 : Conversation State

## Position dans le bootcamp

Ce jour appartient à la **Semaine 2 — AI Agent Development**.

Sujet de la journée : **J4 Conversation State**.

Les jours précédents ont posé les bases suivantes :

- **J1 Architecture d’un agent** : boucle agentique, rôle du modèle, outils, observations et décision.
- **J2 Function Calling** : un modèle peut demander l’exécution d’un outil avec des arguments structurés.
- **J3 Structured Outputs** : une réponse IA peut être contrainte par un contrat de données validable.

Cette journée introduit une brique indispensable pour les agents multi-tours : le **Conversation State**.

## Objectif général

Construire un agent qui ne traite pas chaque message comme un événement isolé.

À la fin de la journée, l’apprenant sait :

- expliquer pourquoi un agent stateless échoue dans une conversation réelle ;
- distinguer historique, état courant, slots métier, résultat d’outil et mémoire ;
- concevoir un état conversationnel minimal mais robuste ;
- mettre à jour l’état à chaque tour utilisateur ;
- détecter les champs manquants ;
- générer la prochaine question à partir de l’état ;
- sérialiser et restaurer une conversation ;
- éviter les fuites d’état entre utilisateurs.

## Livrables du jour

```text
book/week02/day04/
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
│   ├── conversation_state_lifecycle.mmd
│   └── stateful_agent_sequence.mmd
├── assets/
│   ├── manifest.json
│   └── conversation_state_schema.json
└── labs/
    ├── README.md
    ├── conversation_state_agent.py
    └── test_conversation_state_agent.py
```

Notebooks générés :

```text
notebooks/week02/S2_J4_conversation_state.ipynb
notebooks/week02/teacher/S2_J4_conversation_state_teacher.ipynb
```

## Projet fil rouge

Le lab construit un mini-agent de support client capable de collecter progressivement les informations nécessaires à un traitement métier.

Exemple :

```text
Utilisateur : Je veux un remboursement.
Assistant : Quel est votre numéro de commande ?
Utilisateur : ORD-1001
Assistant : Quelle adresse email est associée à la commande ?
Utilisateur : lea@example.com
Assistant : Quelle est la raison du remboursement ?
Utilisateur : J’ai été facturée deux fois.
Assistant : Merci, j’ai les informations nécessaires pour transmettre la demande.
```

Le point important n’est pas la qualité linguistique de l’assistant. Le point important est la capacité du système à maintenir un état fiable entre les tours.

## Pourquoi ce jour est important

Un agent IA backend doit souvent fonctionner sur plusieurs tours :

- l’utilisateur donne des informations partielles ;
- l’agent pose une question ciblée ;
- un outil retourne un résultat ;
- l’utilisateur corrige une information ;
- le système doit savoir ce qui est déjà connu ;
- la logique métier doit continuer sans repartir de zéro.

Sans état conversationnel, l’agent risque de :

- redemander les mêmes informations ;
- oublier une intention déjà détectée ;
- mélanger les données de deux utilisateurs ;
- appeler un outil avec des arguments incomplets ;
- produire une réponse incohérente ;
- rendre les tests difficiles.

Le Conversation State transforme une conversation en processus contrôlable :

```text
message utilisateur
→ extraction
→ mise à jour de l’état
→ validation
→ décision de prochaine action
→ réponse
```

## Prérequis

- Avoir terminé Semaine 2 — Jour 1 : Architecture d’un agent.
- Avoir terminé Semaine 2 — Jour 2 : Function Calling.
- Avoir terminé Semaine 2 — Jour 3 : Structured Outputs.
- Comprendre les dictionnaires Python.
- Savoir lire une dataclass.
