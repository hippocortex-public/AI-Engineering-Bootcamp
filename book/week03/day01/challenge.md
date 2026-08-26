# Challenge — Assistant multi-agents de support SaaS

## Contexte

Une entreprise SaaS veut traiter des tickets entrants :

- facturation ;
- bug technique ;
- sécurité ;
- demande produit ;
- remboursement ;
- demande ambiguë.

L’assistant doit router, déléguer, produire une réponse, demander clarification si nécessaire, faire valider la réponse et enregistrer une trace.

## Mission

Concevoir une architecture multi-agents complète.

## Livrables attendus

1. Schéma d’architecture.
2. Liste des agents.
3. Rôle de chaque agent.
4. Entrées/sorties de chaque agent.
5. Règles de routage.
6. Règles de handoff.
7. Règles de partage d’état.
8. Erreurs possibles.
9. Métriques de qualité.
10. Stratégie de test.

## Contraintes

- Maximum six agents.
- Rôles distincts.
- Reviewer limité à la validation.
- Données sensibles non partagées par défaut.
- Demandes ambiguës → clarification.
- Décisions de routage structurées.

## Critères de réussite

Le design est réussi si les responsabilités sont non ambiguës, les interactions traçables, les limites explicites et les tests réalisables sans LLM réel.
