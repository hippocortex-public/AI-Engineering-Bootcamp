# Review formateur — Jour 6 — Context Engineering

## Résumé pédagogique

Cette journée fait passer les apprenants d’une vision simple du prompt à une vision système du contexte.

Point clé :

```text
Le contexte est un artefact d’architecture, pas une concaténation de messages.
```

## Concepts à vérifier

L’apprenant doit savoir expliquer :

- différence entre memory, state et context ;
- rôle du budget ;
- sélection d’outils ;
- ressources MCP ;
- visibilité ;
- PII ;
- déduplication ;
- trace des décisions.

## Déroulé conseillé

1. Revenir sur le jour 5 : état partagé.
2. Montrer qu’un état partagé n’est pas automatiquement un contexte modèle.
3. Présenter le concept de context pack.
4. Faire les exercices 1 à 3.
5. Exécuter le lab.
6. Modifier le budget pour observer les rejets.
7. Ajouter un élément privé et vérifier qu’il ne fuite pas.
8. Faire le challenge en binôme.

## Erreurs fréquentes

- Confondre mémoire longue et contexte.
- Injecter tout l’historique.
- Donner tous les outils à tous les agents.
- Oublier les raisons de rejet.
- Ne pas tester les cas de fuite.
- Penser uniquement en tokens et pas en permissions.

## Questions de relance

- Quel contexte supprimerais-tu en premier ?
- Que faire si un document critique dépasse le budget ?
- Comment auditer la sélection ?
- Pourquoi un outil disponible n’est-il pas toujours un outil exposé ?
- Que doit voir un reviewer que le coder ne voit pas ?

## Critères de validation

Le lab est validé si :

- les tests passent ;
- le budget est respecté ;
- la visibilité est appliquée ;
- les doublons sont supprimés ;
- la PII est réduite ;
- le rendu final est lisible ;
- les rejets sont traçables.

## Propositions d’amélioration

Ces propositions ne modifient pas les spécifications figées.

- Ajouter une version avancée avec scoring sémantique.
- Ajouter un tokenizer réel.
- Ajouter un exemple MCP avec ressources distantes.
- Ajouter une visualisation du budget par couche.
