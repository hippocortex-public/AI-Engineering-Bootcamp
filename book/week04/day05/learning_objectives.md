# Learning objectives

À la fin de cette journée, l'étudiant doit être capable de :

## Compréhension

- expliquer le rôle d'un workflow engine dans un mini-framework d'agents ;
- distinguer boucle agentique, workflow déterministe et orchestration multi-agents ;
- identifier les responsabilités qui ne doivent pas rester dans les prompts ;
- décrire un workflow comme un graphe d'étapes dépendantes ;
- expliquer les statuts `pending`, `running`, `completed`, `failed`, `blocked` et `skipped`.

## Conception

- concevoir un contrat `WorkflowDefinition` ;
- modéliser une étape avec handler, dépendances, condition, retry et sensibilité ;
- définir un état d'exécution sérialisable ;
- prévoir les comportements d'erreur et de retry ;
- intégrer des points d'approbation humaine ;
- produire une trace exploitable.

## Implémentation

- implémenter un moteur d'exécution topologique ;
- détecter les dépendances inconnues, doublons et cycles ;
- enregistrer des handlers de workflow ;
- exécuter un workflow de support déterministe ;
- tester les chemins heureux et les chemins d'erreur ;
- exporter le résultat en JSON.

## Niveau attendu

L'objectif n'est pas de construire Airflow, Temporal ou LangGraph. L'objectif est de comprendre les invariants d'un workflow engine d'agents :

- contrat explicite ;
- ordre contrôlé ;
- état observable ;
- erreurs maîtrisées ;
- sécurité avant action sensible ;
- tests reproductibles.
