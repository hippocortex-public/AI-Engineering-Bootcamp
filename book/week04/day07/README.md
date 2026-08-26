# Semaine 4 — Jour 7 : Intégration du mini-framework d'agents

## Position dans le bootcamp

Cette journée clôture la semaine 4, consacrée à l'**AI Framework Engineering**.

Après avoir construit séparément :

- l'architecture du framework ;
- l'abstraction `Agent` ;
- le `ToolRegistry` ;
- la `MemoryLayer` ;
- le `WorkflowEngine` ;
- l'observabilité ;

ce jour intègre ces briques dans un mini-framework cohérent, testable et extensible.

## Objectif du jour

Construire une première version intégrée d'un framework d'agents capable de :

1. déclarer des agents ;
2. enregistrer des outils ;
3. maintenir une mémoire utilisateur ;
4. exécuter un workflow déterministe ;
5. produire des traces exploitables ;
6. appliquer des garde-fous sur les actions sensibles ;
7. retourner un résultat structuré.

## Résultat attendu

À la fin de la journée, l'apprenant possède une base de framework utilisable pour orchestrer un agent applicatif simple.

Le framework n'est pas encore un produit de production. Il est volontairement pédagogique, mais respecte les principes attendus d'un système AI Engineering :

- contrats explicites ;
- validation locale ;
- séparation des responsabilités ;
- traces ;
- tests ;
- absence de dépendance cachée ;
- exécution reproductible.

## Fichiers principaux

```text
book/week04/day07/
├── chapter.md
├── exercises.md
├── interview.md
├── challenge.md
├── labs/
│   ├── integration_lab.py
│   └── test_integration.py
└── corriges/

mini_framework/
└── integration.py
```

## Lien avec la semaine 5

La semaine 5 abordera les systèmes IA en production. Cette journée sert de transition : avant d'exposer un agent via API, Redis, PostgreSQL ou monitoring externe, il faut disposer d'un noyau interne propre.
