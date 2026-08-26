# Lab — Memory courte, longue et state

## Objectif

Implémenter un mini-agent de support qui combine :

- une mémoire courte bornée ;
- un état de conversation ;
- une mémoire longue par utilisateur ;
- une personnalisation contrôlée ;
- une fonction d’oubli.

## Fichiers

```text
labs/
├── memory_agent.py
└── test_memory_agent.py
```

## Exécution

Depuis ce dossier :

```bash
python memory_agent.py
python test_memory_agent.py
```

Le lab n’utilise aucune dépendance externe.

## Scénario

L’utilisateur peut écrire :

```text
Tu peux m'appeler Nadia.
Je préfère les exemples en Python.
J'ai un problème avec Billing API.
```

L’agent doit :

1. mémoriser le nom préféré ;
2. mémoriser la préférence de langage ;
3. garder le produit dans le state courant ;
4. demander la description si elle manque ;
5. ne pas mélanger les profils utilisateurs.

## Ce que le lab ne fait pas

Le lab ne simule pas un LLM.

Il entraîne la couche applicative autour du modèle :

- mémoire ;
- state ;
- contexte ;
- tests ;
- isolation.

## Extension recommandée

Après avoir terminé le lab, ajouter une `MemoryPolicy` qui refuse explicitement les secrets et produit un journal d’audit.
