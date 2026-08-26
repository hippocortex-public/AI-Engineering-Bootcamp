# Semaine 4 — Jour 5 : Workflow Engine

## Position dans le bootcamp

La semaine 4 construit progressivement un mini-framework d'agents. Après l'architecture, l'abstraction `Agent`, le `Tool Registry` et la `Memory Layer`, ce jour introduit le composant qui orchestre l'exécution : le **Workflow Engine**.

Un workflow engine transforme une intention métier en un graphe d'étapes contrôlées. Il ne doit pas être confondu avec une simple boucle agentique. La boucle agentique décide au fil de l'eau ; le workflow engine impose un contrat d'exécution, des dépendances, des statuts et des points de contrôle.

## Problème traité

Un agent de production doit souvent exécuter plusieurs opérations dans un ordre cohérent :

1. classifier une demande ;
2. récupérer ou construire le contexte ;
3. choisir un plan ;
4. exécuter des outils ;
5. demander une validation humaine si l'action est sensible ;
6. produire une réponse finale ;
7. tracer ce qui s'est passé.

Sans moteur de workflow, cette logique finit souvent dispersée dans des prompts, des handlers et des conditions implicites. Le résultat devient difficile à tester, à déboguer et à faire évoluer.

## Livrables du jour

- définition du rôle d'un workflow engine dans un framework d'agents ;
- modélisation d'un workflow comme graphe d'étapes ;
- moteur synchrone déterministe en Python standard library ;
- gestion des dépendances, retries, conditions et approbations ;
- traces structurées ;
- tests unitaires ;
- notebook étudiant ;
- notebook formateur avec corrections.

## Ce que l'étudiant construit

Le lab construit un moteur de workflow pédagogique capable d'exécuter un workflow de support IA :

```text
classify -> enrich -> plan -> refund? -> final_answer
```

L'étape `refund` est conditionnelle et sensible. Elle ne s'exécute que si le plan la demande et si une approbation humaine est fournie.

## Compétence AI Engineering

À la fin de la journée, l'étudiant sait expliquer pourquoi un workflow engine est un composant central entre :

- l'agent ;
- les outils ;
- la mémoire ;
- les garde-fous ;
- l'observabilité ;
- l'expérience utilisateur.
