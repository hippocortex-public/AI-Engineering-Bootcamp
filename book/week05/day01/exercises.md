# Exercices

## Exercice 1 — Prototype ou production ?

Classe chaque architecture dans `prototype`, `pré-production` ou `production`.

### Architecture A

```text
Streamlit -> OpenAI API -> réponse
```

### Architecture B

```text
FastAPI -> Agent Runtime -> Model Gateway -> OpenAI API
                 |
                 +-> Tool Gateway
                 +-> Observability
                 +-> State Store
```

### Architecture C

```text
Cron -> Script Python -> LLM -> Email client
```

Pour chaque architecture, donne : catégorie, risques principaux et amélioration minimale.

## Exercice 2 — Identifier les frontières

Cas d’usage :

> Un assistant support peut lire les tickets, proposer une réponse et déclencher un remboursement après validation humaine.

Liste les composants nécessaires et explique leurs responsabilités.

## Exercice 3 — Découper l’état

Classe les éléments suivants dans `conversation state`, `memory`, `business database` ou `observability`.

1. Dernier message utilisateur.
2. Préférence utilisateur : “réponds en français”.
3. Numéro de commande.
4. Trace d’un appel outil.
5. Statut actuel : `waiting_for_human_approval`.
6. Historique des remboursements.
7. Latence d’un appel modèle.
8. Slot collecté : `ticket_id`.

## Exercice 4 — Readiness checklist

Construis une checklist de mise en production pour un agent de support.

Elle doit couvrir sécurité, fiabilité, coûts, observabilité, qualité, données et rollback.

## Exercice 5 — Blueprint minimal

Écris un blueprint JSON minimal contenant au moins 8 composants, 2 stores, 2 gateways, 4 risques et 6 contrôles production.
