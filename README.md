# AI Engineering Bootcamp

**From Backend Developer to AI Solution Architect**

Ce dépôt accompagne un parcours complet d'AI Engineering orienté agents IA, architecture, production, workflow engineering, évaluation, gouvernance et RAG.

L'objectif n'est pas seulement d'apprendre des bibliothèques, mais de construire progressivement une plateforme IA complète et documentée.

## Objectifs

À la fin du bootcamp, ce dépôt contiendra :

- un livre structuré en chapitres Markdown ;
- des notebooks générés depuis les chapitres ;
- un mini framework d'agents développé progressivement ;
- une plateforme IA prête pour la production ;
- des exemples reproductibles ;
- des tests unitaires et d'intégration ;
- des diagrammes d'architecture ;
- une documentation publiable avec MkDocs.

## Public cible

Ce bootcamp s'adresse principalement à des profils :

- développeur backend ;
- architecte logiciel ou solution ;
- ingénieur DevOps / platform engineer ;
- développeur souhaitant évoluer vers AI Backend Engineer ou AI Solution Architect.

## Roadmap

| Bloc | Thème | Objectif |
|---|---|---|
| 1 | Foundations of AI Engineering | Comprendre les LLM |
| 2 | AI Agent Development | Construire un agent |
| 3 | Multi-Agent & MCP | Faire collaborer plusieurs agents |
| 4 | AI Framework Engineering | Construire un mini framework |
| 5 | Production AI Systems | Concevoir une architecture IA prête pour la production |
| 6 | Frameworks du marché | Comparer LangGraph, OpenAI Agents SDK, CrewAI, ADK |
| 7 | Workflow Engineering | Orchestrer des workflows robustes |
| 8 | AI Engineering Ops | Évaluer, observer, gouverner |
| 9 | Knowledge Systems | RAG moderne |
| 10 | NLP appliqué | Extraction, classification, embeddings |
| 11 | Projet final | Plateforme IA complète |

## Structure du dépôt

```text
ai-engineering-bootcamp/
├── book/
├── notebooks/
├── mini_framework/
├── ai_platform/
├── examples/
├── tests/
├── docs/
├── diagrams/
└── scripts/
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,docs]"
```

## Générer les notebooks

```bash
python scripts/build_notebooks.py
```

## Lancer les tests

```bash
pytest
```

## Lancer la documentation

```bash
mkdocs serve
```
