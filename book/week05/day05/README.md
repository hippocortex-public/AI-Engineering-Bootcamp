# Semaine 5 — Jour 5 : Monitoring des systèmes IA en production

## Position dans le bootcamp

La semaine 5 construit les fondations d’un système IA exploitable en production : architecture, API, cache Redis, persistance PostgreSQL, monitoring, sécurité et déploiement.

Ce jour 5 est consacré au **monitoring**. L’objectif n’est pas seulement de vérifier qu’une API répond. Un système IA en production doit être observable sur plusieurs dimensions :

- disponibilité de l’API ;
- latence bout-en-bout ;
- erreurs techniques ;
- erreurs fonctionnelles ;
- consommation de tokens ;
- coût estimé ;
- qualité des réponses ;
- dérive de comportement ;
- saturation des dépendances ;
- incidents exploitables par une équipe.

## Problème traité

Une application IA peut paraître saine au niveau HTTP tout en étant dégradée côté métier.

Exemples :

- le modèle répond toujours `200 OK`, mais hallucine davantage ;
- les coûts doublent à cause de prompts trop longs ;
- la latence augmente uniquement pour certains types de requêtes ;
- une dépendance externe ralentit sans provoquer d’erreur explicite ;
- les réponses refusées ou vides augmentent progressivement ;
- un agent boucle trop longtemps avant de produire une réponse.

Le monitoring d’un système IA doit donc combiner **observabilité logicielle classique** et **métriques spécifiques aux LLM**.

## Livrables de la journée

À la fin de la journée, l’apprenant sait concevoir et implémenter un socle minimal de monitoring pour une API IA :

- métriques techniques ;
- métriques IA ;
- endpoint `/metrics` ;
- endpoint `/health` ;
- règles d’alerte ;
- estimation de coûts ;
- journalisation structurée ;
- redaction de données sensibles ;
- tests automatisés sur la logique de monitoring.

## Lab

Le lab construit une mini-API FastAPI instrumentée :

```text
labs/monitoring_ai_service/
├── app.py
├── metrics.py
├── alerts.py
├── cost.py
├── redaction.py
├── schemas.py
└── tests/
```

Le lab n’appelle pas de vrai modèle externe. Il simule une réponse IA afin que le monitoring reste reproductible, testable et exécutable localement.

## Pré-requis

- Python 3.11+
- bases de FastAPI
- bases de Redis et PostgreSQL vues les jours précédents
- notions de latence, erreurs HTTP et logs applicatifs

## Résultat attendu

L’apprenant doit être capable d’expliquer, coder et tester un système de monitoring minimal pour une API IA en production.

## Parcours conseillé — 60 minutes

1. Objectifs et chapitre : 20 minutes.
2. Installation et lab : 20 minutes.
3. Exercices et diagnostic : 15 minutes.
4. Correction et questions d'entretien : 5 minutes.

Le challenge constitue un approfondissement facultatif. Commencer par
`learning_objectives.md`, puis `chapter.md` et `labs/README.md`.

## Intégration au dépôt

Copier les fichiers de cette archive en conservant les autres jours. Aucun fichier
`__init__.py` partagé du mini-framework n'est remplacé. Les notebooks de la journée
sont fournis dans `notebooks/week05/`. Le lab est autonome ; son raccordement aux
services réels des jours 2 à 4 reste un travail d'intégration explicite.
