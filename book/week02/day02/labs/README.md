# Lab — Function Calling Agent

Ce lab contient une implémentation locale et exécutable d’un mini-agent de support client utilisant le pattern Function Calling.

## Fichiers

```text
function_calling_agent.py
test_function_calling_agent.py
```

## Exécution

Depuis la racine du dépôt :

```bash
python book/week02/day02/labs/function_calling_agent.py
python book/week02/day02/labs/test_function_calling_agent.py
```

## Objectif

Comprendre la boucle suivante :

1. un message utilisateur est reçu ;
2. un planificateur simulé produit un appel d’outil ;
3. le registre valide l’appel ;
4. la fonction métier est exécutée ;
5. le résultat est retourné sous forme structurée ;
6. l’agent produit une réponse finale.

## Remarque

Le lab n’utilise volontairement aucun fournisseur LLM externe. Cela permet de tester l’architecture sans réseau, sans clé API et sans non-déterminisme.
