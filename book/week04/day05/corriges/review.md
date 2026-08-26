# Review notes — Jour 5

## Objectif pédagogique atteint

L'étudiant doit repartir avec l'idée qu'un workflow engine est une couche de contrôle, pas une simple fonction utilitaire.

## Points clés à vérifier

- L'étudiant sait lire un graphe de dépendances.
- L'étudiant sait expliquer pourquoi les actions sensibles sont bloquées sans approbation.
- L'étudiant comprend que `skipped` n'est pas une erreur.
- L'étudiant sait lire une trace.
- L'étudiant sait distinguer workflow state et memory layer.

## Erreurs fréquentes

### 1. Confondre retry et boucle infinie

Un retry est borné, tracé et justifié. Une boucle infinie est un défaut d'architecture.

### 2. Rendre l'étape finale trop permissive

Si une action critique échoue ou est bloquée, la réponse finale ne doit pas faire croire que tout est résolu.

### 3. Mettre la sécurité dans le prompt

Le prompt peut expliquer la politique. Le moteur doit l'appliquer.

### 4. Oublier les tests de graphe

Un workflow invalide ne doit jamais démarrer.

## Questions de consolidation

- Où placerais-tu une étape d'évaluation automatique ?
- Comment reprendrais-tu un workflow interrompu ?
- Comment stockerais-tu les traces ?
- Comment éviterais-tu un double remboursement lors d'un retry ?
- Quelles étapes devraient être parallélisées en production ?

## Transition vers le jour 6

Le jour 6 ajoute l'observabilité. Le workflow engine produit déjà des traces ; il faut maintenant structurer ces signaux pour le debugging, le monitoring, l'évaluation et la supervision opérationnelle.
