# Notes formateur — Semaine 1 Jour 6

## Intention pédagogique

Cette journée fait la transition entre compréhension conceptuelle des LLM et intégration logicielle.

Le point central est le passage :

```text
prompt libre -> contrat applicatif
```

## Points à renforcer en session

- Le modèle propose, l'application dispose.
- Un JSON valide n'est pas une vérité métier.
- Les outils doivent être peu nombreux, explicites et contrôlés.
- Les tests déterministes précèdent les appels réels.
- Le Jour 7 branchera ces patterns sur un client Python.

## Risques pédagogiques

Les apprenants peuvent croire que Tool Calling signifie que le modèle exécute réellement une fonction. Corriger immédiatement : le modèle émet une intention structurée, l'application exécute après validation.
