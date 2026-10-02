# Semaine 5 — Jour 6 : Sécurité des systèmes IA en production

## Position dans le parcours

Après l'architecture, FastAPI, Redis, PostgreSQL et le monitoring, ce jour construit
les frontières de sécurité du service IA. Le jour 7 sera consacré au déploiement,
conformément à la roadmap figée.

## Résultat attendu

Construire une API qui authentifie l'appelant, vérifie ses permissions, isole les
documents par tenant et refuse les outils non autorisés. Un tenant représente ici
une organisation cliente ; un sujet identifie un appelant dans cette organisation.

Le lab est autonome, sans fournisseur LLM, sans cloud, sans Redis ni PostgreSQL.
Le modèle est simulé pour vérifier des règles backend de façon reproductible.
L'intégration aux jours précédents est expliquée dans le chapitre ; elle n'est pas
présentée comme déjà réalisée.

## Parcours de 60 minutes

| Temps | Travail |
|---|---|
| 0–5 min | Lire les objectifs et le scénario de menace |
| 5–25 min | Étudier le chapitre : identité, données, outils, quotas |
| 25–45 min | Exécuter le lab et les scénarios d'accès refusé |
| 45–55 min | Résoudre les exercices 1 à 3 |
| 55–60 min | Comparer les corrigés et répondre à deux questions d'entretien |

Les exercices 4 à 6 et le challenge constituent un approfondissement de 45 à
90 minutes. Ils n'allongent pas implicitement le parcours principal.

## Ordre de lecture

1. `learning_objectives.md`
2. `chapter.md`
3. `labs/README.md`
4. `exercises.md`, puis `corriges/exercises_solution.md`
5. `interview.md`, puis `corriges/interview_solution.md`
6. `challenge.md`, puis `corriges/challenge_solution.md`

Les notebooks étudiant et enseignant sont dans `notebooks/week05/` à la racine
du dépôt. Le notebook enseignant contient aussi les notes de revue.

## Prérequis

Python 3.11+, bases de FastAPI et tests HTTP, compréhension des jours 2 à 5.
L'expérience Spring Security est utile : une dépendance FastAPI établit ici un
principal de confiance, puis une politique vérifie ses droits avant le service métier.

## Intégration de l'archive

Ajouter `book/week05/day06/` et les deux notebooks. Aucun module partagé du
mini-framework et aucun `__init__.py` des jours précédents ne sont remplacés.
La `ROADMAP.md` racine fournie est une copie inchangée du contrat du plugin.
Fusionner l'entrée J6 des fichiers de suivi avec ceux de votre dépôt plutôt que
remplacer leur historique. Le ZIP est un incrément du jour 6, pas le dépôt complet.

## Critères de réussite

- Sans clé valide : 401 ; avec une permission insuffisante : 403.
- Une ressource d'un autre tenant reste inaccessible par toutes les routes.
- Un outil inconnu est refusé, même demandé dans un prompt.
- Le quota est partagé entre routes et clés d'une même identité.
- Les logs ne contiennent ni clés, ni prompts, ni documents.
- La configuration absente ou invalide empêche le démarrage.
