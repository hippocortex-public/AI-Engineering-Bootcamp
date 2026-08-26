# Semaine 2 — Jour 2 : Function Calling

## Position dans le bootcamp

Ce jour appartient à la **Semaine 2 — AI Agent Development**.

Sujet de la journée : **J2 Function Calling**.

Le jour précédent a introduit l’architecture générale d’un agent. Cette journée transforme cette architecture en système capable d’agir : le modèle ne se contente plus de produire du texte, il sélectionne une fonction, fournit des arguments structurés, puis l’application exécute cette fonction de manière contrôlée.

## Objectif général

Construire un agent capable d’utiliser des outils applicatifs via un contrat explicite de function calling.

À la fin de la journée, l’apprenant sait :

- définir un outil sous forme de contrat ;
- exposer ce contrat à un modèle ;
- valider les arguments d’un appel de fonction ;
- router l’appel vers une fonction Python ;
- réinjecter le résultat dans la conversation ;
- distinguer ce que décide le modèle de ce que contrôle l’application.

## Livrables du jour

```text
book/week02/day02/
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
│   ├── function_calling_loop.mmd
│   └── tool_registry_sequence.mmd
├── assets/
│   └── support_tools_schema.json
└── labs/
    ├── README.md
    ├── function_calling_agent.py
    └── test_function_calling_agent.py
```

Notebooks générés :

```text
notebooks/week02/S2_J2_function_calling.ipynb
notebooks/week02/teacher/S2_J2_function_calling_teacher.ipynb
```

## Prérequis

- Savoir expliquer le rôle d’un agent IA.
- Comprendre la différence entre modèle, application et outil.
- Être à l’aise avec des fonctions Python simples.
- Connaître les bases de JSON.

## Fil rouge

Le fil rouge est un **assistant de support client mono-agent**.

L’utilisateur pose une question sur une commande. Le modèle choisit l’outil à appeler. L’application valide l’appel, exécute le bon outil, puis renvoie le résultat au modèle ou à l’utilisateur.

Exemples d’outils :

- récupérer le statut d’une commande ;
- estimer un remboursement ;
- créer un ticket de support.

## Résultat attendu

À la fin du jour, l’apprenant dispose d’un mini-agent local et exécutable qui simule une boucle de function calling sans dépendre d’une API externe. Ce choix permet de comprendre le mécanisme fondamental avant d’utiliser un fournisseur LLM réel.

## À retenir

Le function calling n’est pas une exécution magique par le modèle.

Le modèle propose un appel structuré.  
L’application garde le contrôle de l’exécution.
