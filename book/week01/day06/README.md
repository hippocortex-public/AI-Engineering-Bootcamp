# Semaine 1 — Jour 6 — API modernes : Responses API, Structured Outputs, Tool Calling

## Position dans la semaine

La Semaine 1 pose les fondations de l'AI Engineering. Après les tokens, la fenêtre de contexte et le Prompt Engineering, cette journée montre comment un système logiciel dialogue avec un modèle via une API moderne.

Le sujet du jour est volontairement orienté ingénierie : il ne s'agit pas seulement d'appeler un LLM, mais de construire des appels reproductibles, validables, observables et intégrables dans un backend.

## Objectifs du jour

À la fin de cette journée, l'apprenant doit savoir :

- distinguer une API de complétion historique d'une API orientée réponses ;
- structurer une requête modèle avec instructions, entrée, format de sortie et outils ;
- utiliser un schéma de sortie pour réduire l'ambiguïté ;
- concevoir une boucle simple de Tool Calling ;
- expliquer pourquoi la validation applicative reste obligatoire ;
- préparer le terrain du Jour 7 : premier client Python.

## Artefacts

- `learning_objectives.md`
- `chapter.md`
- `exercises.md`
- `corriges/exercises_solutions.md`
- `interview.md`
- `challenge.md`
- `references.md`
- `labs/lab_modern_api_patterns.md`
- `diagrams/*.mmd`
- `assets/api_request_example.json`
- `notebooks/week01/day06/modern_api_patterns.ipynb`
- `examples/week01/day06/modern_api_patterns.py`
- `tests/week01/day06/test_modern_api_patterns.py`

## Prérequis

- Comprendre le rôle d'un prompt système et d'un prompt utilisateur.
- Savoir lire un objet JSON.
- Avoir des bases Python : fonctions, dictionnaires, exceptions.
- Avoir compris la notion de token et de fenêtre de contexte.

## Résultat attendu

L'apprenant construit une mini-couche Python qui simule trois briques essentielles :

1. une requête de type Responses API ;
2. une sortie structurée validée ;
3. un appel d'outil contrôlé côté application.
