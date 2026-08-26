# Corrigé — Interview

## Réponse 1

La short-term memory conserve le contexte récent. Le conversation state décrit la tâche en cours. La long-term memory conserve des informations stables et réutilisables dans de futures conversations.

## Réponse 2

Il ne faut pas stocker tout l’historique car cela augmente le coût, ajoute du bruit, conserve potentiellement des données sensibles et rend la mémoire difficile à gouverner.

## Réponse 3

On isole la mémoire par identifiant utilisateur ou tenant. Les clés de stockage doivent inclure `user_id`, et les tests doivent vérifier qu’une préférence utilisateur n’est jamais visible pour un autre.

## Réponse 4

Une information promue vers la mémoire longue doit être explicite, stable, utile, non sensible et révocable.

## Réponse 5

Le conversation state est limité à une tâche. Il ne conserve pas nécessairement les préférences réutilisables entre sessions.

## Réponse 6

On teste la couche mémoire avec du code déterministe : ajout de messages, extraction simulée, mise à jour de profil, construction de contexte et suppression.

## Réponse 7

`forget_user(user_id)` doit supprimer le profil, l’historique court associé, les états actifs liés à l’utilisateur et les journaux d’audit éventuels.

## Réponse 8

Un résumé de conversation compresse des échanges récents ou passés. Une mémoire longue représente des faits ou préférences sélectionnés selon une politique.

## Réponse 9

Une politique explicite évite que des informations temporaires, sensibles ou inférées deviennent des vérités durables.

## Réponse 10

Il faut traiter la confidentialité, la rétention, la suppression, l’audit, le consentement, la sécurité, le contrôle utilisateur et la conformité.

## Réponse 11

Structured Outputs peut forcer l’extraction mémoire à produire un objet validable comme `{should_store, key, value, reason, confidence}`.

## Réponse 12

Une mémoire trop agressive peut personnaliser à tort, conserver des données sensibles, amplifier des erreurs et diminuer la confiance utilisateur.
