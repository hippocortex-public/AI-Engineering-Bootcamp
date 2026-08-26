# Review formateur — Jour 3 Semaine 3

## Intention pédagogique

Cette journée transforme l’idée de tool calling en une compétence d’architecture.

Les apprenants doivent comprendre qu’un serveur MCP n’est pas un détail d’intégration, mais une frontière technique entre l’agent et le système métier.

## Points à surveiller

Les erreurs fréquentes :

- confondre tool et resource ;
- exposer des fonctions trop internes ;
- oublier la validation côté serveur ;
- retourner des exceptions Python brutes ;
- laisser un tool sensible sans approbation ;
- créer des noms d’outils non compréhensibles par un modèle ;
- ignorer les traces.

## Questions à poser en revue

1. Que se passe-t-il si le modèle invente un argument ?
2. Qui est responsable de refuser une action dangereuse ?
3. Pourquoi `resources/read` ne doit pas modifier le système ?
4. Comment feriez-vous évoluer ce serveur pour plusieurs équipes ?
5. Quelle différence avec un simple dictionnaire Python de fonctions ?

## Critères de validation

L’étudiant doit pouvoir :

- expliquer le flux `tools/list` puis `tools/call` ;
- lire et modifier le schéma d’un tool ;
- ajouter une resource ;
- ajouter un prompt ;
- interpréter une erreur JSON-RPC ;
- justifier les garde-fous de `refund_order`.

## Propositions d’amélioration

Ces propositions ne modifient pas les spécifications figées du bootcamp.

- Ajouter plus tard un transport stdio réel.
- Ajouter un exemple HTTP local.
- Ajouter une couche d’authentification.
- Ajouter un outil d’audit plus avancé.
- Ajouter un exercice de menace autour de l’indirect prompt injection.
