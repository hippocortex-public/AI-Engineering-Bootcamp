# Challenge — Construire un agent support client minimal

## Contexte

Tu construis un assistant IA mono-agent pour un service client e-commerce.

L’agent doit traiter trois types de demandes :

1. statut d’une commande ;
2. disponibilité d’un produit ;
3. demande générale.

## Contraintes

Tu dois implémenter l’agent sans framework externe.

Tu peux utiliser uniquement la bibliothèque standard Python.

## Architecture attendue

Ton code doit contenir :

- une structure `AgentState` ;
- une fonction `decide_action` ;
- un outil `lookup_order` ;
- un outil `lookup_inventory` ;
- une fonction `run_agent` ;
- une trace d’exécution ;
- au moins trois tests simples avec `assert`.

## Entrées à supporter

```text
Où est ma commande 123 ?
Le produit SKU-42 est-il disponible ?
Bonjour, pouvez-vous m’aider ?
```

## Résultat attendu

L’agent doit retourner :

- une réponse finale lisible ;
- l’action sélectionnée ;
- une trace d’exécution.

## Critères d’évaluation

- L’architecture est claire.
- Les responsabilités sont séparées.
- Le code est exécutable.
- Les traces sont utiles.
- Les cas principaux sont testés.
- L’agent reste simple et compréhensible.
