# Objectifs pédagogiques — Jour 3

## Objectifs principaux

À la fin de cette journée, l’apprenant saura :

1. Expliquer le rôle d’un serveur MCP dans une architecture d’agents.
2. Distinguer tools, resources et prompts.
3. Modéliser un tool comme contrat d’entrée/sortie.
4. Implémenter un serveur MCP minimal avec des méthodes JSON-RPC.
5. Valider les arguments reçus avant exécution.
6. Retourner des erreurs structurées plutôt que des exceptions brutes.
7. Ajouter des garde-fous sur les actions sensibles.
8. Produire une trace d’exécution exploitable.
9. Préparer un serveur MCP pour une intégration client au jour suivant.

## Compétences AI Engineering

Cette journée développe les compétences suivantes :

- conception de contrats d’intégration ;
- séparation agent / tool / système métier ;
- exposition contrôlée de capacités applicatives ;
- validation stricte des entrées ;
- observabilité minimale ;
- sécurité par design ;
- testabilité d’une interface agentique.

## Ce qui n’est pas encore couvert

Cette journée ne traite pas encore :

- l’implémentation d’un client MCP complet ;
- le transport réseau réel ;
- l’authentification OAuth ;
- les serveurs MCP distribués ;
- la connexion à un LLM réel.

Ces sujets seront introduits progressivement dans les journées suivantes.

## Critères de réussite

L’apprenant réussit la journée s’il peut :

- lancer le lab ;
- lister les tools disponibles ;
- appeler un tool valide ;
- provoquer et comprendre une erreur de validation ;
- lire une resource ;
- récupérer un prompt ;
- expliquer pourquoi un serveur MCP n’est pas simplement une collection de fonctions Python.
