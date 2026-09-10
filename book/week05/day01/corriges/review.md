# Review formateur

## Résumé

Cette journée marque le passage du framework interne vers une plateforme IA exploitable en production.

Message central :

> La production IA est une discipline d’architecture, pas seulement d’intégration API.

## Points à vérifier

Un apprenant doit pouvoir :

- dessiner une architecture en couches ;
- identifier les frontières critiques ;
- expliquer le rôle du model gateway ;
- expliquer le rôle du tool gateway ;
- distinguer state, memory et database ;
- proposer des contrôles de coût ;
- définir des traces utiles ;
- construire une checklist de mise en production.

## Erreurs fréquentes

### Appeler directement le modèle depuis l’API

Correction : introduire un service applicatif, injecter un runtime, passer par un model gateway et tracer l’appel.

### Confondre mémoire et base métier

La mémoire agentique ne doit jamais devenir la source officielle pour les tickets, commandes ou paiements.

### Oublier les actions sensibles

Tout outil qui modifie un état externe doit être traité comme sensible.

### Ne pas versionner les contrats IA

Un changement de prompt peut avoir autant d’impact qu’un changement de code.

## Critère de validation

La journée est réussie si l’apprenant peut défendre une architecture compréhensible par un backend engineer, un security engineer, un product manager, un SRE et un AI engineer.
