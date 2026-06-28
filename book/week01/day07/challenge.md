# Challenge — Mini client LLM réutilisable

## Objectif

Construire un client Python minimal mais propre, capable de :

1. générer du texte ;
2. générer une sortie JSON validée ;
3. fonctionner en mode mock ;
4. être testé automatiquement.

## Contexte

Tu travailles sur la mini-bibliothèque de la Semaine 1. Elle doit bientôt intégrer :

- tokenisation ;
- embeddings ;
- appel LLM ;
- démonstration CLI.

Le Jour 7 doit produire la brique `LLMClient`.

## Contraintes

Le code doit :

- utiliser des dataclasses ;
- ne pas appeler le réseau dans les tests ;
- injecter le transport ;
- définir des erreurs spécifiques ;
- exposer une méthode `generate_text`;
- exposer une méthode `generate_json`;
- inclure au moins trois tests.

## Critères d’acceptation

Le challenge est réussi si :

- `pytest` passe ;
- le client fonctionne avec `MockTransport`;
- une réponse JSON valide est parsée ;
- une réponse JSON invalide déclenche une erreur ;
- le code reste lisible et extensible.

## Bonus

Ajoute un transport réel optionnel basé sur le SDK OpenAI, activé uniquement si la dépendance est installée et si `OPENAI_API_KEY` existe.
