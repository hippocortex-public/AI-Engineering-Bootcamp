# Corrigé — Questions d'entretien

## Réponse 1

Mettre la logique agentique dans les routes mélange transport, métier et orchestration.  
Cela rend le code difficile à tester, à monitorer, à réutiliser et à remplacer.

Une route doit valider, contrôler et déléguer.

## Réponse 2

`healthz` vérifie que le processus répond.  
`readyz` vérifie que l'application peut réellement traiter du trafic.

Une API peut être vivante mais non prête si une dépendance critique est indisponible.

## Réponse 3

Un `request_id` permet de corréler la requête HTTP, les logs, les appels modèle, les appels outils, les erreurs et les traces.  
Sans cet identifiant, le debug production devient lent et imprécis.

## Réponse 4

En entreprise, on peut utiliser OAuth2, JWT, mTLS, API gateway, IAM cloud ou service mesh.  
Le choix dépend du périmètre : utilisateurs finaux, services internes, partenaires ou backoffice.

## Réponse 5

Valider avant d'appeler un modèle réduit les coûts, évite les entrées dangereuses, améliore les erreurs client et protège les dépendances internes.

## Réponse 6

Un rate limiter en mémoire ne fonctionne pas correctement avec plusieurs processus, plusieurs pods ou plusieurs régions.  
Il ne survit pas au redémarrage et ne permet pas une gouvernance centralisée.

## Réponse 7

Tester OpenAPI permet de vérifier que le contrat public de l'API expose bien les routes prévues.  
C'est utile pour les clients générés, la documentation et les gateways.

## Réponse 8

Une erreur utilisateur vient d'une requête invalide.  
Une erreur de modèle vient du fournisseur ou de la sortie du modèle.  
Une erreur d'outil vient d'une dépendance appelée par l'agent.

Les trois doivent être distinguées pour diagnostiquer correctement le système.
