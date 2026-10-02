# Semaine 5 — Jour 7 : Déploiement d'un système IA

## Position dans la semaine

Ce jour termine la semaine Production AI Systems : architecture, FastAPI, Redis,
PostgreSQL, monitoring, sécurité, puis déploiement. Il suit la roadmap figée du plugin.
La prochaine semaine porte sur les frameworks du marché ; elle n'est pas ajoutée ici.

## Livrable opérationnel

Un lab autonome réunissant une API FastAPI, PostgreSQL et Redis dans Docker Compose.
L'API conserve l'identité et l'isolation par tenant, utilise un cache partitionné,
externalise les quotas dans Redis et expose des métriques Prometheus protégées.
Le fournisseur LLM est simulé ; aucun compte cloud ni clé de fournisseur n'est requis.

## Parcours principal — 60 minutes

| Durée | Activité |
|---|---|
| 5 min | Objectifs, architecture et critères d'acceptation |
| 15 min | Chapitre : image, configuration, sondes, données, rollback |
| 25 min | Installation, démarrage Compose et smoke tests |
| 10 min | Exercices 1 à 3 et comparaison aux corrigés |
| 5 min | Questions d'entretien et checklist de livraison |

Le téléchargement initial des images et dépendances peut allonger le temps de lab.
Les exercices 4–5 et le challenge sont des approfondissements de 30 à 60 minutes.
Sans Docker, exécuter les tests Python ; ils ne remplacent pas le démarrage de la stack.

## Ordre de travail

Lire `learning_objectives.md`, `chapter.md`, puis `labs/README.md`. Le cours explique
les compromis, le README du lab contient les commandes. Les exercices, entretiens
et challenge ont leurs corrigés dans `corriges/`. Deux notebooks sont fournis dans
`notebooks/week05/` à la racine, avec génération depuis Markdown.

## Intégration au dépôt

Ajouter uniquement le jour 7 et ses notebooks. Le lab n'écrase pas les modules des
jours précédents ni les fichiers `__init__.py` partagés. Il reprend les principes
J2–J6 dans un service indépendant afin de pouvoir être lancé sans réunir les anciens ZIP.
Le fichier auth local dérive du jour 6 et ajoute un scope d'exploitation `metrics:read`.

Fusionner les entrées des fichiers de suivi racine avec l'historique existant.
La roadmap fournie est inchangée. Cette archive est un incrément, pas une copie
intégrale du dépôt.

## Critères de réussite

- API exécutée par un utilisateur non root ; données hors image.
- DB et Redis sans ports publiés ; API limitée à localhost pour le lab.
- Secrets absents de l'image et montés uniquement dans les services nécessaires.
- Readiness contrôlant schéma PostgreSQL et disponibilité Redis.
- Lecture alpha autorisée, beta refusée, cache sans contournement d'ACL.
- Quota atomique partagé et refus contrôlé si Redis est indisponible.
- Smoke tests, procédure de release et rollback compris.

Voir `assets/validation_report.md` pour distinguer les contrôles exécutés des
vérifications Docker restant à effectuer sur votre machine.
