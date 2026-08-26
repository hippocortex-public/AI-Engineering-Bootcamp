# Objectifs pédagogiques — Jour 6 — Context Engineering

## Objectifs principaux

À la fin de cette journée, l’apprenant doit être capable de :

1. définir le rôle du Context Engineering dans un système agentique ;
2. distinguer prompt engineering, memory management et context engineering ;
3. construire un contexte minimal pour un objectif donné ;
4. appliquer un budget de tokens approximatif ;
5. filtrer les informations selon leur visibilité ;
6. prioriser les éléments de contexte ;
7. supprimer les doublons ;
8. réduire les informations sensibles avant injection ;
9. produire un contexte traçable ;
10. expliquer comment MCP influence la sélection de contexte.

## Objectifs techniques

L’apprenant doit savoir implémenter :

- un modèle de données pour les éléments de contexte ;
- une politique de contexte ;
- un moteur de sélection ;
- un rendu textuel structuré ;
- des tests de non-régression ;
- une stratégie de refus ou de clarification quand le contexte est insuffisant.

## Résultats attendus

L’apprenant doit pouvoir répondre aux questions suivantes :

- Que faut-il envoyer au modèle ?
- Que faut-il garder hors du modèle ?
- Qu’est-ce qui relève de l’état applicatif ?
- Qu’est-ce qui relève de la mémoire longue ?
- Quand faut-il récupérer une ressource MCP ?
- Quand faut-il résumer ou supprimer un élément ?
- Comment expliquer une décision de sélection de contexte ?

## Critères de maîtrise

La journée est maîtrisée si l’apprenant peut :

- construire un context pack sous budget ;
- justifier chaque élément inclus ;
- identifier les fuites de contexte possibles ;
- réduire le bruit informationnel ;
- préserver les éléments critiques ;
- écrire des tests garantissant que les informations privées ne sont pas injectées par erreur.
