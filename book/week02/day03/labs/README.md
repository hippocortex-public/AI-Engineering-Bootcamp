# Lab — Structured Output Agent

## Objectif

Construire un mini-agent de triage support fondé sur une sortie structurée.

Le lab montre comment passer de :

```text
ticket utilisateur
```

à :

```text
objet métier validé
```

sans dépendance externe.

## Fichiers

```text
structured_output_agent.py
test_structured_output_agent.py
```

## Exécution

Depuis le dossier `book/week02/day03/labs/` :

```bash
python structured_output_agent.py
python test_structured_output_agent.py
```

## Ce que le lab démontre

- Un schéma JSON peut être traité comme un contrat.
- Une sortie modèle doit être parsée puis validée.
- Le mapping vers un objet métier doit se faire uniquement après validation.
- Les tests négatifs protègent le backend contre les sorties imprévisibles.
- La réponse utilisateur doit rester séparée de la donnée machine.

## Limite volontaire

Le lab utilise un `MockStructuredModel`.

Il ne dépend pas d’un fournisseur LLM afin que la logique d’architecture soit testable localement.
