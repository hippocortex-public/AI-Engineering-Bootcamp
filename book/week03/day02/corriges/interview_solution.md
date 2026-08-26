# Corrigé — Questions d'entretien — Coordination multi-agents

## Question 1

La coordination est distincte parce qu'un agent spécialiste produit une réponse locale, alors que le coordinateur gère le système global : sélection des agents, ordre d'exécution, contexte partagé, conflits, limites, revue et trace.

## Question 2

Router consiste à choisir le bon agent ou les bons agents.  
Un handoff transfère le contrôle conversationnel à un autre agent.  
Le routing peut rester interne au manager, alors que le handoff change l'agent actif.

## Question 3

Partager tout le contexte augmente les coûts, introduit du bruit, peut exposer des informations inutiles, dégrade le focus et rend le debug plus difficile. Cela peut aussi créer des réponses contaminées par des informations qui ne concernent pas l'agent.

## Question 4

On peut détecter un conflit en comparant les statuts, les décisions, les contraintes ou les affirmations critiques. Dans un système simple, des statuts incompatibles comme `resolved` et `unresolved` suffisent à déclencher un conflit.

## Question 5

Un reviewer doit être déclenché en cas de risque élevé, désaccord, action sensible, manque d'information, domaine sécurité/juridique ou réponse externe engageante.

## Question 6

Les limites de tours évitent les boucles infinies, réduisent les coûts, améliorent la prévisibilité et forcent le système à produire un statut final clair.

## Question 7

On peut remplacer les agents LLM par des agents déterministes en Python. Chaque agent retourne une observation stable. Les tests vérifient la sélection, les conflits, la revue, la trace et le statut final.

## Question 8

Une trace doit contenir la tâche, les agents sélectionnés, les décisions de routing, les appels d'agents, les observations, les conflits, la revue éventuelle, la synthèse et le statut final.

## Question 9

Un manager-worker centralise la décision. Il est donc plus facile d'inspecter qui a été appelé, pourquoi, dans quel ordre et avec quel résultat. Un réseau libre de handoffs peut être plus flexible mais plus difficile à auditer.

## Question 10

Il faut isoler la politique de coordination des outils concrets. MCP peut ensuite fournir des tools, resources ou prompts, mais le coordinateur doit continuer à manipuler des contrats : tâche, plan, observation, conflit, résultat.
