# Semaine 7 — Workflow Engineering

Cette archive ajoute les sept journées de la semaine 7. La roadmap source regroupe n8n, orchestration, événements, workflows hybrides et human in the loop; elle ne prescrit pas de découpage journalier. Les sept unités proposées détaillent ces thèmes sans modifier la roadmap.

| Jour | Sujet | Preuve principale |
|---|---|---|
| 1 | n8n et frontières | Accusé de réception durable |
| 2 | Orchestration et état | Reprise d’un job |
| 3 | Événements et contrats | Doublon et collision |
| 4 | Fiabilité | Backoff, dead letter, replay |
| 5 | Workflow hybride | Port de génération et validation |
| 6 | Human in the loop | Approbation liée au brouillon |
| 7 | Projet intégré | Parcours et branches d’échec |

Prévoir 1 heure par jour pour le parcours essentiel, ou 2 à 3 heures pour chaque unité complète. Le premier lancement n8n ajoute du temps d’installation.

Fil rouge : événement de support → brouillon simulé → validation humaine → publication locale simulée. Aucun envoi externe et aucun appel LLM dans les labs obligatoires.

## Installation dans le dépôt existant

Décompresser dans un répertoire temporaire. Copier les répertoires `book/week07`, `notebooks/week07`, `examples/week07`, `tests/week07`, `docs/week07` et le script `scripts/generate_week07_notebooks.py` dans leurs homologues du dépôt. Vérifier d’éventuels fichiers S7 existants avant de les remplacer. L’archive ne contient aucun remplacement de README racine, pyproject, mini_framework/__init__.py ou ai_platform/__init__.py.

Le Markdown reste la source de vérité. [QUICKSTART.md](QUICKSTART.md) décrit les commandes; [VALIDATION.md](VALIDATION.md) distingue les contrôles exécutés des vérifications locales n8n.

## Propositions d’amélioration

Outbox et dispatcher pour les effets externes; identité OIDC et contrôle par ressource; claim/lease pour plusieurs workers; jitter, âge des jobs et quotas; adaptateur LLM évalué; portail de revue. Ces propositions ne modifient aucune spécification et ne sont pas présentées comme implémentées.
