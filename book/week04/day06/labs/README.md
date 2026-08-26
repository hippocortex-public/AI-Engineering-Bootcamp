# Lab — Observability Layer

## Objectif

Construire et tester une couche d'observabilité pour le mini-framework d'agents.

Le lab utilise uniquement la bibliothèque standard Python.

## Fichiers

```text
labs/
├── README.md
├── observability_lab.py
└── test_observability.py
```

Le module réutilisable du framework est :

```text
mini_framework/observability.py
```

## Commandes

Depuis la racine du livrable :

```bash
python -m py_compile mini_framework/observability.py book/week04/day06/labs/observability_lab.py book/week04/day06/labs/test_observability.py
python book/week04/day06/labs/test_observability.py
```

## Résultat attendu

```text
15 tests passed
```

## Scénario

Le scénario simule un assistant support qui :

1. ouvre une trace ;
2. classe l'intention ;
3. recherche un ticket ;
4. bloque une action sensible ;
5. produit une réponse sûre ;
6. exporte les traces, événements et métriques.
