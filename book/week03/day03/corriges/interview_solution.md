# Corrigé — Questions d’entretien MCP Server

## Réponse 1

MCP résout le problème de standardisation de la frontière entre agents et capacités applicatives. Il évite que chaque agent intègre directement des fonctions internes avec un format propriétaire.

## Réponse 2

Un tool est une action invocable. Une resource est une donnée consultable. Un tool peut produire un effet ; une resource devrait généralement rester en lecture.

## Réponse 3

Le modèle peut se tromper, halluciner un champ ou fournir un type incorrect. La validation doit donc rester côté serveur, car le serveur est responsable de l’intégrité du système métier.

## Réponse 4

Je le traiterais comme un tool sensible : confirmation humaine obligatoire, contrôle de montant, idempotence, audit log, vérification des permissions et vérification de l’éligibilité métier.

## Réponse 5

Une trace doit inclure l’identifiant de requête, la méthode, le tool appelé, le statut, la durée, l’erreur éventuelle et éventuellement l’identité du client ou de l’utilisateur.

## Réponse 6

Trop d’outils augmentent le bruit contextuel, les mauvais choix du modèle et la surface d’attaque. Il vaut mieux exposer une surface petite, claire et fortement documentée.

## Réponse 7

Je documenterais chaque tool, je stabiliserais les noms, je séparerais les capabilities par domaine et j’ajouterais des garde-fous pour que différents agents puissent utiliser le serveur sans casser les règles métier.

## Réponse 8

Une erreur protocolaire concerne la requête elle-même : méthode inconnue, paramètres invalides, JSON mal formé. Une erreur métier concerne le domaine : commande inexistante, remboursement impossible, limite dépassée.

## Réponse 9

Risques principaux : prompt injection indirecte via resources, exfiltration de données, actions sensibles non approuvées, tools trop permissifs, secrets exposés dans les descriptions ou les schémas, absence d’audit.

## Réponse 10

On peut tester le serveur avec des requêtes JSON déterministes. Il suffit d’appeler `initialize`, `tools/list`, `tools/call`, `resources/read` et de vérifier les réponses sans connecter de modèle.
