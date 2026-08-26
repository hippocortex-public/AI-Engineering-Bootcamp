# Objectifs pédagogiques — Jour 6

## Objectifs principaux

À la fin de cette journée, l'apprenant doit être capable de :

1. Expliquer ce qu'est une boucle agentique.
2. Décrire les étapes `plan`, `act`, `observe`, `decide`.
3. Distinguer planification initiale et replanification.
4. Implémenter une boucle agentique déterministe en Python.
5. Ajouter une limite d'itérations pour éviter les boucles infinies.
6. Journaliser les décisions de l'agent pour faciliter le debugging.
7. Mettre à jour un état conversationnel ou métier après chaque observation.
8. Évaluer si une tâche est terminée ou doit continuer.
9. Tester une boucle agentique sans dépendre d'un appel LLM réel.

## Objectifs AI Engineering

L'apprenant doit comprendre qu'une boucle agentique robuste est une construction logicielle, pas seulement un prompt.

Un agent de production doit être :

- **borné** : nombre maximum d'itérations ;
- **observable** : journal d'étapes et traces ;
- **testable** : comportement reproductible ;
- **composable** : outils et politiques séparés ;
- **sûr** : refus des actions inconnues ou risquées ;
- **maintenable** : état explicite, formats documentés.

## Pré-requis

L'apprenant doit avoir compris :

- le function calling ;
- les Structured Outputs ;
- le state conversationnel ;
- la mémoire court terme et long terme.

## Ce que cette journée ne couvre pas

Cette journée ne couvre pas encore :

- les architectures multi-agents ;
- les handoffs entre agents spécialisés ;
- MCP ;
- les workflows distribués ;
- l'observabilité de production complète.

Ces sujets arrivent plus tard dans la roadmap.
