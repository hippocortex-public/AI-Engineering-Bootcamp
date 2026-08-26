# Semaine 4 — Jour 4 : Memory Layer

## Position dans le bootcamp

La semaine 4 construit progressivement un mini-framework d'agents. Après l'architecture, l'abstraction `Agent` et le `Tool Registry`, ce jour ajoute une **Memory Layer** réutilisable.

Une couche mémoire n'est pas un simple historique de messages. Dans un framework d'agents, elle définit un contrat d'ingénierie pour stocker, filtrer, retrouver, oublier et injecter des informations dans le contexte d'exécution.

## Objectif du jour

Construire une couche mémoire minimale mais production-shaped :

- isolation par namespace ;
- types de mémoire ;
- visibilité `private`, `shared`, `public` ;
- expiration TTL ;
- récupération déterministe ;
- politique de redaction PII ;
- snapshot JSON ;
- journal d'audit ;
- intégration possible dans un runner d'agent.

## Livrables

```text
book/week04/day04/
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

mini_framework/
└── memory.py

notebooks/week04/
├── S4_J4_memory_layer.ipynb
└── teacher/
    └── S4_J4_memory_layer_teacher.ipynb
```

## Lab

Le lab implémente `MemoryStore`, `MemoryRecord`, `MemoryQuery` et un mécanisme de recherche transparent basé sur :

- overlap lexical ;
- tags ;
- importance ;
- propriétaire agent ;
- filtres de visibilité ;
- expiration.

```bash
cd book/week04/day04/labs
python memory_layer_lab.py
python test_memory_layer.py
```

## Résultat attendu

À la fin de la journée, l'apprenant sait concevoir une mémoire d'agent qui peut être utilisée dans un mini-framework sans fuite de contexte, sans mémoire globale implicite et sans dépendance externe.
