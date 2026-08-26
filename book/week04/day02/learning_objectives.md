# Objectifs pédagogiques — Abstraction Agent

À la fin de cette journée, l’apprenant saura :

## Objectifs conceptuels

1. Expliquer pourquoi un agent doit être une abstraction stable et non un simple script.
2. Identifier les responsabilités qui appartiennent à l’agent et celles qui doivent rester hors de l’agent.
3. Décrire la relation entre `Agent`, `ModelClient`, `RunContext`, `AgentResult` et `Runner`.
4. Expliquer pourquoi l’injection de dépendance rend un agent testable.
5. Concevoir une interface compatible avec de futurs ajouts : tools, mémoire, workflows et observabilité.

## Objectifs pratiques

1. Créer une classe `Agent` configurable.
2. Valider une configuration d’agent.
3. Construire un prompt système + utilisateur de manière déterministe.
4. Exécuter un agent avec un faux modèle local.
5. Retourner une réponse structurée contenant texte, statut, usage estimé et trace.
6. Bloquer une exécution non conforme via des guardrails simples.
7. Écrire des tests unitaires couvrant les comportements attendus.

## Compétences AI Engineering

- API design ;
- séparation des responsabilités ;
- testabilité ;
- contrats d’exécution ;
- dépendance injectée ;
- préparation à l’orchestration ;
- design incrémental d’un framework.
