# Semaine 9 — Jour 4 : Hybrid Search : BM25 et fusion des rangs

Calculer un classement lexical BM25 sur le corpus autorisé.

Parcours essentiel : 60 minutes (cours 20 min, lab 25 min, exercice 10 min, synthèse 5 min). Prévoir 2 à 3 heures pour l’unité complète avec entretien et challenge. Les modèles et services optionnels ajoutent un temps d’installation distinct.

Prérequis : Python 3.11+, JSON, notions de vecteurs et de persistance. Le parcours obligatoire utilise uniquement la bibliothèque standard et ne contacte aucun service externe.

Lire [les objectifs](learning_objectives.md), [le chapitre](chapter.md), puis [le lab](labs/README.md). Réaliser [les exercices](exercises.md), [l’entretien](interview.md) et [le challenge](challenge.md) avant les corrigés locaux.

Notebooks depuis la racine : `notebooks/week09/S9_J4_hybrid_search.ipynb` et `notebooks/week09/teacher/S9_J4_hybrid_search_teacher.ipynb`.

Critère de réussite : Mesurer la couverture des candidats avant de choisir un top-k.

Les calculs de retrieval et de persistance sont exécutables; le corpus est fictif. L’encodeur de base est lexical et la réponse finale est extractive. Les extensions neuronales sont séparées et n’ont pas été exécutées ici.
