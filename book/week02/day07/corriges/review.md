# Review formateur — Jour 7

## Objectif de la review

Valider que les apprenants ont compris qu'un agent autonome professionnel est un système contrôlé, observable et testable.

## Points à vérifier

- L'agent ne confond pas autonomie et absence de règles.
- Les actions sensibles sont bloquées sans validation.
- L'état est explicite.
- Les tâches sont observables.
- Les conditions d'arrêt existent.
- Les tests couvrent succès et échecs.
- Les traces permettent de comprendre les décisions.

## Questions de débrief

1. Qu'est-ce qui empêcherait cet agent d'être mis en production tel quel ?
2. Où placeriez-vous l'appel LLM réel dans cette architecture ?
3. Quelles décisions doivent rester déterministes ?
4. Quelles données devraient être persistées ?
5. Quelles traces seraient utiles pour le monitoring ?

## Réponses attendues

Un bon apprenant doit répondre que :

- le LLM peut aider à créer ou ajuster le plan ;
- l'exécution des outils doit rester contrôlée ;
- les validations sensibles doivent être côté orchestrateur ;
- l'état doit pouvoir être sauvegardé ;
- les traces doivent être consultables ;
- les tests doivent isoler le comportement métier du modèle.

## Checklist de complétude

- [x] README présent.
- [x] Objectifs pédagogiques présents.
- [x] Chapitre présent.
- [x] Exercices présents.
- [x] Interview présent.
- [x] Challenge présent.
- [x] Références présentes.
- [x] Corrigés présents.
- [x] Diagrammes présents.
- [x] Assets présents.
- [x] Lab présent.
- [x] Notebook étudiant présent.
- [x] Notebook formateur présent.
- [x] Tests exécutables.
