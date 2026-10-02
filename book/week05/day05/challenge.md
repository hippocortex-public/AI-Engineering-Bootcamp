# Challenge — Construire un monitoring minimal pour une API IA

## Contexte

Tu travailles sur une API `/chat` utilisée par une équipe produit. L’API appelle un modèle IA et retourne une réponse à l’utilisateur.

Depuis quelques jours, l’équipe observe trois problèmes :

1. certains utilisateurs se plaignent de lenteurs ;
2. la facture LLM augmente ;
3. quelques réponses sont vides, mais l’API retourne quand même `200 OK`.

Tu dois concevoir un monitoring minimal pour rendre ces problèmes visibles.

## Objectif

Créer un système de monitoring applicatif capable de :

- enregistrer chaque requête IA ;
- mesurer latence, statut HTTP, tokens, coût et réponses vides ;
- exposer un snapshot de métriques ;
- déclencher des alertes simples ;
- éviter de logger des secrets.

## Contraintes

- Le système doit être testable sans fournisseur LLM réel.
- Le stockage en mémoire est accepté pour le challenge.
- Les prompts bruts ne doivent pas être conservés dans les métriques.
- Les règles d’alerte doivent être lisibles.
- Le code doit être séparé en composants.

## Attendus

Le rendu doit inclure :

1. un modèle de données pour représenter une requête monitorée ;
2. un collecteur de métriques ;
3. une fonction de calcul de coût ;
4. au moins trois règles d’alerte ;
5. une fonction de redaction ;
6. des tests unitaires ;
7. une courte explication de l’architecture.

## Bonus

Ajouter :

- un endpoint `/health` ;
- un endpoint `/metrics` ;
- une route `/chat` simulée ;
- un `request_id` retourné au client ;
- un runbook associé à chaque alerte.
