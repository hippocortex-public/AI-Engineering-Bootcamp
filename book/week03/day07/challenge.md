# Challenge — Jour 7 — Projet multi-agent

## Objectif

Étendre le lab pour construire un **assistant multi-agent de préparation de livraison logicielle**.

L’assistant doit recevoir un objectif comme :

> Préparer une livraison d’API avec documentation, tests, analyse des risques et plan de rollback.

## Contraintes

Votre solution doit :

1. ajouter un agent `qa`;
2. ajouter un outil `generate_release_checklist`;
3. produire au moins quatre artefacts ;
4. refuser les actions sensibles sans approbation humaine ;
5. maintenir un état partagé versionné ;
6. produire une trace JSON ;
7. déclencher une revue finale ;
8. retourner un statut contrôlé parmi :
   - `completed`;
   - `needs_revision`;
   - `needs_clarification`;
   - `blocked_by_policy`.

## Livrables attendus

Vous devez fournir :

- le code modifié ;
- les tests associés ;
- un exemple de sortie JSON ;
- une courte justification d’architecture.

## Critères d’évaluation

La solution est réussie si :

- les responsabilités des agents sont séparées ;
- les outils sont validés avant exécution ;
- le contexte transmis à chaque agent est limité ;
- la revue finale ne dépend pas de l’agent producteur ;
- la sortie est traçable ;
- les tests couvrent les cas de succès et d’échec.
