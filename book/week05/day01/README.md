# Semaine 5 — Jour 1 : Architecture production

## Position dans le bootcamp

La semaine 5 transforme les agents, MCP et le mini-framework construits précédemment en **système IA de production**.

Roadmap : Semaine 5 — Production AI Systems, Jour 1 — Architecture production.

## Objectif du jour

Concevoir une architecture backend fiable, observable, sécurisée et exploitable pour une plateforme IA.

## Résultat attendu

À la fin de la journée, l’apprenant sait :

- distinguer prototype, framework interne et plateforme de production ;
- identifier les composants obligatoires d’une architecture IA backend ;
- définir les frontières entre API, orchestration, modèle, outils, mémoire, données et observabilité ;
- raisonner en termes de fiabilité, latence, coûts, sécurité et exploitation ;
- produire un blueprint d’architecture validable automatiquement.

## Lab

```bash
python book/week05/day01/labs/production_architecture_lab.py
python book/week05/day01/labs/test_production_architecture.py
```

## Package amorcé

```text
ai_platform/
├── __init__.py
└── architecture.py
```

Le `__init__.py` est cumulatif par conception : les prochains jours devront ajouter leurs exports sans supprimer ceux du jour 1.
