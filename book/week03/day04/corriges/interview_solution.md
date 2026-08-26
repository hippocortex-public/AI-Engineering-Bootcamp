# Corrigé — Questions d'entretien MCP Client

## Question 1

Un client MCP est la couche qui connecte l'orchestrateur ou l'agent à un serveur MCP. Il initialise la session, découvre les capabilities, expose les tools localement, valide les arguments, appelle les méthodes MCP et convertit les résultats en observations exploitables.

## Question 2

Sans couche cliente dédiée, l'agent devient couplé au protocole, au transport et aux formats d'erreur. Cela rend le système plus fragile, plus difficile à tester et plus difficile à sécuriser.

## Question 3

Une erreur locale de validation est détectée avant l'appel serveur, par exemple un argument obligatoire manquant. Une erreur serveur MCP vient de la réponse du serveur, par exemple un tool inconnu ou une erreur d'exécution.

## Question 4

Le client appelle `tools/list`, convertit chaque tool en spécification locale, puis crée une fonction wrapper par tool. Chaque wrapper appelle `client.call_tool(tool_name, arguments)`.

## Question 5

Le cache peut devenir dangereux si les tools, schémas, permissions ou politiques serveur changent. Il faut prévoir une invalidation manuelle, TTL ou invalidation sur erreur.

## Question 6

On instrumente le client avec des traces contenant request id, méthode, tool, arguments filtrés, statut, durée, erreur éventuelle et métadonnées de session.

## Question 7

Le client doit bloquer avant le serveur si les arguments sont invalides, si le tool n'est pas autorisé, si une action sensible manque d'approbation ou si une politique de sécurité échoue.

## Question 8

Une action sensible doit passer par une politique explicite : approbation humaine, rôle utilisateur, seuils, audit, traçabilité et éventuellement confirmation multi-étape.
