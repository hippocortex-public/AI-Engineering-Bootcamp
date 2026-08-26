# Semaine 4 — Jour 6 : Observabilité

## Position dans le bootcamp

La semaine 4 construit progressivement un mini-framework d'agents. Après l'architecture, l'abstraction `Agent`, le `Tool Registry`, la `Memory Layer` et le `Workflow Engine`, ce jour ajoute une couche transversale : **l'observabilité**.

L'objectif n'est pas seulement de logger du texte. Un framework d'agents doit permettre de répondre à des questions d'exploitation :

- quelle étape a échoué ?
- quel outil a été appelé ?
- combien de temps a duré chaque span ?
- quelles données sensibles ont été masquées ?
- quelle décision a conduit à une action ?
- quelles métriques permettent de suivre la fiabilité ?

## Livrables du jour

- un chapitre complet sur l'observabilité des systèmes agentiques ;
- des exercices progressifs ;
- un challenge de conception ;
- des questions d'entretien ;
- des corrections locales ;
- deux diagrammes Mermaid ;
- un lab Python exécutable sans dépendance externe ;
- un module `mini_framework/observability.py` réutilisable ;
- un notebook étudiant ;
- un notebook formateur.

## Mini-framework

Le module ajouté est :

```text
mini_framework/
└── observability.py
```

Il fournit :

- `Observability`;
- `ObservabilityConfig`;
- `TraceRecord`;
- `SpanRecord`;
- `EventRecord`;
- `MetricPoint`;
- redaction de données sensibles ;
- export JSON ;
- résumé de métriques ;
- rapport de santé d'une trace.

## Commandes de validation

Depuis la racine du livrable :

```bash
python -m py_compile mini_framework/observability.py book/week04/day06/labs/observability_lab.py book/week04/day06/labs/test_observability.py
python book/week04/day06/labs/test_observability.py
```

## Résultat attendu

```text
15 tests passed
```
