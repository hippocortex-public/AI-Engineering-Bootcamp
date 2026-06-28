# Semaine 1 — Jour 5 : Prompt Engineering

## Position dans la roadmap

Semaine 1 : **Foundations of AI Engineering**  
Jour 5 : **Prompt Engineering**

Objectif de la semaine : comprendre le fonctionnement des LLM et savoir utiliser une API moderne de manière raisonnée.

Le Jour 5 fait le lien entre la compréhension interne des LLM étudiée les jours précédents et leur utilisation pratique dans des systèmes logiciels. Après avoir étudié l'histoire des modèles, les embeddings, l'attention, les tokens, BPE et la fenêtre de contexte, cette journée formalise l'art de transformer un besoin métier en instruction exploitable par un modèle.

## Objectif de la journée

À la fin de cette journée, l'apprenant sait :

- concevoir un prompt robuste pour une tâche d'AI Engineering ;
- distinguer instruction, contexte, contraintes, exemples et format de sortie ;
- écrire des prompts testables, versionnables et maintenables ;
- identifier les limites du prompt engineering ;
- construire un mini-banc d'évaluation local pour comparer plusieurs prompts sans dépendre d'une API externe.

## Livrables

Ce dossier contient :

- `README.md` : vue d'ensemble de la journée ;
- `learning_objectives.md` : objectifs pédagogiques détaillés ;
- `chapter.md` : cours principal ;
- `exercises.md` : exercices guidés ;
- `corriges/solutions.md` : corrigés complets ;
- `interview.md` : questions d'entretien ;
- `challenge.md` : challenge de fin de journée ;
- `references.md` : références et lectures complémentaires ;
- `diagrams/prompt_pipeline.mmd` : diagramme Mermaid du pipeline de prompt ;
- `assets/prompt_template.md` : template réutilisable ;
- `labs/prompt_evaluator.py` : lab Python exécutable ;
- `labs/sample_tasks.json` : dataset local de test ;
- `notebooks/week01/day05_prompt_engineering.ipynb` : notebook généré depuis le Markdown.

## Pré-requis

- Semaine 1 Jour 3 : Transformer et Attention ;
- Semaine 1 Jour 4 : Tokens, BPE et fenêtre de contexte ;
- Python 3.10+ pour exécuter le lab ;
- aucune clé API requise pour cette journée.

## Résultat attendu

L'apprenant doit produire un prompt template professionnel, l'évaluer sur plusieurs cas, expliquer ses choix et identifier les risques de mauvaise généralisation.
