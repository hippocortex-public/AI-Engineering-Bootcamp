# Semaine 2 — Jour 5 : Memory courte, longue et state

## Position dans le bootcamp

Ce jour appartient à la **Semaine 2 — AI Agent Development**.

Sujet de la journée : **J5 Memory (courte, longue, state)**.

Les jours précédents ont posé les bases suivantes :

- **J1 Architecture d’un agent** : boucle agentique, rôle du modèle, outils, observations et décision.
- **J2 Function Calling** : le modèle peut demander l’exécution d’outils avec des arguments structurés.
- **J3 Structured Outputs** : la sortie peut respecter un contrat de données validable.
- **J4 Conversation State** : l’agent suit une tâche multi-tours avec des slots, un statut et des champs manquants.

Cette journée ajoute une couche décisive : la **mémoire d’agent**.

## Objectif général

Construire un agent capable de distinguer ce qui doit être conservé seulement pendant quelques tours, ce qui décrit l’état courant de la tâche, et ce qui peut être retenu durablement pour personnaliser les prochaines interactions.

À la fin de la journée, l’apprenant sait :

- distinguer **short-term memory**, **conversation state** et **long-term memory** ;
- expliquer pourquoi l’historique brut ne suffit pas ;
- concevoir une mémoire courte sous contrainte de fenêtre de contexte ;
- concevoir une mémoire longue orientée profil utilisateur ;
- éviter la fuite de mémoire entre utilisateurs ;
- sérialiser et restaurer une mémoire applicative ;
- définir des règles de promotion d’une information vers la mémoire longue ;
- implémenter un agent mémoire déterministe et testable.

## Livrables du jour

```text
book/week02/day05/
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
│   ├── memory_layers.mmd
│   └── memory_promotion_flow.mmd
├── assets/
│   ├── manifest.json
│   └── memory_profile_schema.json
└── labs/
    ├── README.md
    ├── memory_agent.py
    └── test_memory_agent.py
```

Notebooks générés :

```text
notebooks/week02/S2_J5_memory_state.ipynb
notebooks/week02/teacher/S2_J5_memory_state_teacher.ipynb
```

## Projet fil rouge

Le lab construit un assistant de support mémoire-aware.

L’agent doit :

1. garder les derniers messages utiles ;
2. maintenir un état de tâche en cours ;
3. extraire certaines préférences utilisateur ;
4. stocker ces préférences dans une mémoire longue ;
5. isoler strictement les données par utilisateur ;
6. produire une réponse personnalisée sans inventer de mémoire ;
7. permettre l’oubli d’un utilisateur.

## Distinction essentielle

| Concept | Durée | Exemples | Risque principal |
|---|---:|---|---|
| Short-term memory | quelques tours | derniers messages, résumé récent | dépasser la fenêtre de contexte |
| Conversation state | durée de la tâche | intention, slots, statut | déclencher une action avec des champs manquants |
| Long-term memory | durable | nom, préférences, contraintes stables | conserver une donnée sensible ou obsolète |

## Résultat attendu

L’apprenant doit comprendre qu’un agent fiable ne “se souvient” pas par magie.

Il possède une stratégie explicite :

```text
message utilisateur
→ mise à jour de l’historique court
→ mise à jour de l’état courant
→ extraction éventuelle de mémoire durable
→ construction du contexte utile
→ réponse
```

## Critères de réussite

La journée est réussie si l’apprenant peut :

- décrire chaque couche mémoire ;
- justifier ce qui ne doit pas être stocké durablement ;
- écrire des tests d’isolation entre utilisateurs ;
- expliquer le compromis entre résumé, historique brut et mémoire persistante ;
- produire un agent simple qui personnalise une réponse à partir de mémoire validée.

## À ne pas confondre

La mémoire longue n’est pas :

- un dump complet de la conversation ;
- un remplacement de l’état de tâche ;
- une base de données sans politique d’oubli ;
- une preuve de vérité absolue ;
- un endroit pour stocker toute donnée personnelle par défaut.

Elle est un composant applicatif gouverné par des règles explicites.
