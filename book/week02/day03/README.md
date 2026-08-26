# Semaine 2 — Jour 3 : Structured Outputs

## Position dans le bootcamp

Ce jour appartient à la **Semaine 2 — AI Agent Development**.

Sujet de la journée : **J3 Structured Outputs**.

Le jour précédent a introduit le **Function Calling** : le modèle peut choisir une fonction et fournir des arguments structurés que l’application valide avant exécution.

Cette journée complète ce socle avec les **Structured Outputs** : le modèle ne produit plus seulement du texte libre, mais une sortie conforme à un contrat explicite, typée, validable et directement exploitable par le code applicatif.

## Objectif général

Construire une couche de sortie robuste pour un agent IA.

À la fin de la journée, l’apprenant sait :

- concevoir un schéma de sortie orienté produit ;
- différencier JSON libre, JSON mode, function calling et Structured Outputs ;
- définir un contrat de réponse stable ;
- valider une sortie avant usage métier ;
- gérer les erreurs de parsing et de validation ;
- transformer une réponse structurée en décision applicative ;
- préparer le terrain pour le **Conversation State** du jour suivant.

## Livrables du jour

```text
book/week02/day03/
├── README.md
├── learning_objectives.md
├── chapter.md
├── exercises.md
├── interview.md
├── challenge.md
├── references.md
├── corriges/
│   ├── exercises_solution.md
│   ├── interview_solution.md
│   ├── challenge_solution.md
│   └── review.md
├── diagrams/
│   ├── structured_output_pipeline.mmd
│   └── schema_validation_flow.mmd
├── assets/
│   ├── manifest.json
│   └── triage_output_schema.json
└── labs/
    ├── README.md
    ├── structured_output_agent.py
    └── test_structured_output_agent.py
```

Notebooks générés :

```text
notebooks/week02/S2_J3_structured_outputs.ipynb
notebooks/week02/teacher/S2_J3_structured_outputs_teacher.ipynb
```

## Projet fil rouge

Le lab construit un mini-agent de triage support.

L’agent reçoit un ticket client en langage naturel et doit produire une décision structurée :

- catégorie ;
- priorité ;
- sentiment ;
- résumé ;
- action suivante ;
- équipe responsable ;
- niveau de confiance.

L’objectif n’est pas d’appeler un vrai modèle pendant le lab. L’objectif est de comprendre le contrat applicatif qui rend une sortie IA exploitable en production.

## Pourquoi ce jour est important

Un agent IA sans contrat de sortie est difficile à intégrer :

- le backend doit parser du texte fragile ;
- les tests sont instables ;
- les erreurs sont découvertes trop tard ;
- les changements de prompt cassent l’application ;
- les systèmes aval reçoivent des données imprévisibles.

Les Structured Outputs déplacent la complexité vers un contrat explicite :

```text
intention utilisateur
→ raisonnement du modèle
→ sortie conforme à un schéma
→ validation
→ décision applicative
```

## Prérequis

- Avoir terminé Semaine 2 — Jour 1 : Architecture d’un agent.
- Avoir terminé Semaine 2 — Jour 2 : Function Calling.
- Comprendre les bases de JSON.
- Savoir lire une fonction Python simple.
- Comprendre la différence entre texte libre et données structurées.

## Résultat attendu

À la fin du jour, l’apprenant dispose d’un mini-agent local capable de :

1. recevoir un ticket support ;
2. produire une sortie JSON ;
3. valider cette sortie contre un schéma ;
4. convertir la sortie en objet Python ;
5. refuser une sortie invalide ;
6. expliquer pourquoi la validation est une frontière de sécurité applicative.
