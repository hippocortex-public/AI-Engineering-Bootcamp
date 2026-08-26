# Review — Semaine 2 Jour 2

## Synthèse pédagogique

Cette journée introduit le passage d’un agent conversationnel à un agent capable d’utiliser des capacités externes.

Le message clé est :

> Le function calling donne une interface d’action au modèle, mais l’application reste responsable de l’exécution.

## Points maîtrisés attendus

L’apprenant doit savoir :

- décrire la boucle de function calling ;
- écrire un contrat d’outil clair ;
- implémenter un registre d’outils ;
- valider un appel avant exécution ;
- refuser les outils inconnus ;
- traiter les erreurs proprement ;
- tester le comportement sans fournisseur LLM réel.

## Erreurs fréquentes

1. Croire que le modèle exécute lui-même la fonction.
2. Appeler une fonction par son nom avec `globals()`.
3. Oublier `additionalProperties: false`.
4. Utiliser un outil trop générique.
5. Ne pas distinguer outil de lecture et outil d’écriture.
6. Oublier les logs.
7. Confondre function calling et Structured Outputs.

## Questions de vérification rapide

- Que se passe-t-il si le modèle demande un outil inexistant ?
- Où doit vivre la validation : prompt ou application ?
- Pourquoi un outil d’annulation nécessite-t-il une confirmation ?
- Comment tester le dispatch sans LLM ?

## Grille de validation

| Élément | Statut attendu |
|---|---|
| Schémas présents | Oui |
| Registre explicite | Oui |
| Validation stricte | Oui |
| Dispatch contrôlé | Oui |
| Erreurs structurées | Oui |
| Tests exécutables | Oui |
| Notebooks générés | Oui |
| Corrections locales | Oui |

## Préparation du Jour 3

Le Jour 3 introduira les **Structured Outputs**.

Lien naturel avec le Jour 2 :

- Function Calling : le modèle demande une action.
- Structured Outputs : le modèle répond dans un format strict.

Les deux utilisent des schémas, mais servent des objectifs différents.
