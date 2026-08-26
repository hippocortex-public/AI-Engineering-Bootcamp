# Lab — Context Engineering

## Objectif

Construire un moteur simple de Context Engineering capable de sélectionner les éléments utiles à un agent sous contrainte de budget, visibilité et sécurité.

## Fichiers

```text
context_engineering.py
test_context_engineering.py
```

## Exécution

Depuis ce dossier :

```bash
python context_engineering.py
python test_context_engineering.py
```

## Ce que le lab démontre

- sélection de contexte ;
- budget de tokens approximatif ;
- priorisation ;
- déduplication ;
- filtrage par visibilité ;
- filtrage par agent cible ;
- réduction PII ;
- rendu final ;
- audit des éléments rejetés.

## Limite

L’estimation de tokens est volontairement approximative. Elle sert à enseigner le raisonnement de budget sans dépendre d’un tokenizer externe.
