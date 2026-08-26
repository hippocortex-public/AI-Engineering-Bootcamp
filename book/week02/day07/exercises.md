# Exercices

## Exercice 1 — Identifier le type de système

Classe les systèmes suivants :

1. Un chatbot qui répond uniquement par texte.
2. Un assistant qui peut appeler une fonction météo.
3. Un agent qui planifie plusieurs étapes, appelle des outils, observe les résultats et s'arrête.
4. Un workflow n8n déclenché par un webhook.
5. Un agent qui crée automatiquement un remboursement sans validation.

Pour chaque cas, indique :

- type de système ;
- niveau de risque ;
- condition d'arrêt attendue.

## Exercice 2 — Définir un état d'agent

Propose une structure JSON pour représenter l'état d'un agent autonome de réservation de restaurant.

L'état doit contenir :

- l'objectif utilisateur ;
- les champs déjà collectés ;
- les champs manquants ;
- les tâches ;
- le statut ;
- les traces ;
- la réponse finale éventuelle.

## Exercice 3 — Écrire un plan

Pour l'objectif suivant :

```text
Je veux changer l'adresse de livraison de la commande ORDER-1234.
```

Écris un plan en 4 à 6 tâches.

Indique pour chaque tâche :

- son identifiant ;
- son nom ;
- l'outil à utiliser ;
- si l'action est sensible ;
- le statut initial.

## Exercice 4 — Ajouter un garde-fou

Dans le lab, ajoute une règle :

```text
L'agent ne doit pas continuer si budget_used + cost > max_budget.
```

Explique pourquoi cette règle est plus stricte que vérifier seulement `budget_used >= max_budget`.

## Exercice 5 — Tester une action sensible

Écris un test qui vérifie qu'un outil sensible ne s'exécute pas sans approbation humaine.

Le test doit vérifier :

- le statut final ;
- l'entrée manquante ;
- le statut de la tâche bloquée ;
- la présence d'une trace `approval_required`.

## Exercice 6 — Reprise d'exécution

Explique comment utiliser la méthode `AgentState.to_json()` pour sauvegarder un run interrompu, puis `AgentState.from_json()` pour le reprendre.

Donne un exemple de scénario où cette capacité est nécessaire.
