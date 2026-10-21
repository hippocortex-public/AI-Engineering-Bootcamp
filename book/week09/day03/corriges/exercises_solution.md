# Corrigé des exercices

## Exercice 1

Le document est la source courante; les chunks sont ses projections multiples. Cette séparation permet de remplacer un ensemble de chunks atomiquement et de retrouver sa version.

## Exercice 2

Les meilleurs candidats peuvent tous appartenir à un autre tenant. Après filtrage, le résultat peut être vide malgré des passages autorisés pertinents. La recherche doit respecter le périmètre dès son entrée.

## Exercice 3

Les anciens chunks, leurs vecteurs et les citations qui les identifient. Les mémoires liées à l’ancienne version sont masquées; une suppression les retire du store.
