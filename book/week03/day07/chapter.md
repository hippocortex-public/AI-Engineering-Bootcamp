# Chapitre — Projet multi-agent

## 1. Pourquoi un projet intégrateur ?

Les premiers jours de la semaine ont introduit les briques de base :

- une architecture multi-agents ;
- une stratégie de coordination ;
- un serveur MCP ;
- un client MCP ;
- un état partagé ;
- une politique de contexte.

Un système réel ne se contente pas d’empiler ces composants. Il doit les organiser autour d’un objectif métier.

Le projet du jour répond à une question simple :

> Comment construire un système multi-agent qui produit un résultat utile, contrôlé et vérifiable ?

## 2. Le piège du “plus d’agents”

Une erreur fréquente consiste à ajouter des agents pour chaque sous-problème.

Ce n’est pas une architecture. C’est une fragmentation.

Un bon système multi-agent commence par identifier les responsabilités stables :

| Responsabilité | Agent possible |
|---|---|
| Décomposer le travail | Planner |
| Chercher ou extraire le contexte | Researcher |
| Produire une solution technique | Engineer |
| Vérifier les risques | Security |
| Contrôler la qualité | Reviewer |
| Coordonner le tout | Coordinator |

Un agent doit exister seulement si sa responsabilité est claire et si sa sortie est utile à un autre composant.

## 3. Architecture cible

Le projet du jour utilise une architecture **coordinator-led**.

Le coordinateur ne fait pas tout lui-même. Il :

1. reçoit l’objectif ;
2. valide la demande ;
3. crée un plan ;
4. sélectionne les agents ;
5. construit un contexte adapté à chaque agent ;
6. appelle les outils nécessaires ;
7. stocke les résultats dans l’état partagé ;
8. déclenche une revue ;
9. décide si le résultat est acceptable.

Cette architecture est plus simple à auditer qu’un réseau d’agents qui se délèguent librement des responsabilités.

## 4. MCP dans le projet

MCP est utilisé ici comme modèle d’intégration d’outils.

Dans un projet réel, un client MCP peut découvrir les capacités disponibles sur un serveur, puis appeler des tools, lire des resources ou utiliser des prompts.

Dans le lab, l’objectif est pédagogique :

- le serveur MCP est simulé par un registre local ;
- les appels respectent une forme standardisée ;
- chaque outil déclare un schéma d’entrée ;
- le client valide les arguments avant exécution ;
- les outils sensibles sont protégés par approbation humaine.

Cette approche rend le design portable vers un vrai serveur MCP plus tard.

## 5. État partagé

Un projet multi-agent a besoin d’un état partagé, mais cet état ne doit pas devenir un dépôt global incontrôlé.

Le lab distingue trois niveaux de visibilité :

- `private` : visible uniquement par l’agent propriétaire ;
- `shared` : visible par les agents autorisés ;
- `public` : visible par tous les agents du workflow.

Cette séparation limite les fuites de contexte, réduit le bruit et facilite l’audit.

## 6. Context Engineering

Chaque agent reçoit un **context pack** spécifique.

Le contexte n’est pas l’historique complet. C’est une sélection contrôlée de ce qui est utile pour la tâche courante.

Un bon context pack contient :

- l’objectif ;
- la tâche courante ;
- les éléments d’état pertinents ;
- les artefacts disponibles ;
- les contraintes ;
- les outils autorisés ;
- les critères de sortie.

Le lab impose un budget de contexte approximatif en nombre de caractères. Ce budget force à prioriser.

## 7. Boucle de livraison

La boucle de livraison du projet suit le cycle suivant :

```text
objective
  -> plan
  -> assign
  -> build context
  -> call agent
  -> call tools
  -> update shared state
  -> review
  -> final answer
```

La boucle n’est pas infinie. Elle possède :

- une limite d’étapes ;
- des statuts contrôlés ;
- une revue finale ;
- un score minimum ;
- une trace exportable.

## 8. Critères d’acceptation

Le projet est considéré comme réussi si :

- l’objectif utilisateur est validé ;
- un plan est généré ;
- au moins deux agents spécialisés contribuent ;
- les outils nécessaires sont appelés via l’adaptateur MCP ;
- l’état partagé contient les contributions importantes ;
- la revue finale est positive ;
- la trace explique ce qui s’est passé ;
- le résultat final est sérialisable en JSON.

## 9. Ce qui rend l’architecture robuste

Le système devient plus robuste grâce à plusieurs choix :

### Responsabilités séparées

Le planner ne valide pas la sécurité.  
L’engineer ne note pas sa propre production.  
Le reviewer ne modifie pas directement les artefacts.  
Le coordinator orchestre, mais ne remplace pas les spécialistes.

### Interfaces explicites

Les agents échangent des `Task`, `Artifact` et `StateEntry`.

Cela évite les échanges informels impossibles à tester.

### État contrôlé

Chaque entrée d’état possède :

- une clé ;
- une valeur ;
- un propriétaire ;
- une visibilité ;
- une version.

### Outils bornés

Chaque outil possède :

- un nom ;
- une description ;
- un schéma d’entrée ;
- une fonction déterministe ;
- une règle d’approbation si nécessaire.

## 10. Limites pédagogiques

Le lab ne contacte pas de vrai modèle de langage.

C’est volontaire.

Avant de connecter un LLM, il faut comprendre :

- où passe l’état ;
- comment le contexte est construit ;
- qui peut appeler quoi ;
- comment sont validées les entrées ;
- comment sont évalués les résultats ;
- comment déboguer une exécution.

Un LLM peut remplacer les fonctions déterministes du lab, mais il ne doit pas remplacer l’architecture.

## 11. Extension vers production

Pour passer vers un système réel, on pourrait remplacer :

| Composant pédagogique | Équivalent production |
|---|---|
| Fonctions déterministes | Appels LLM |
| Registre local | Serveur MCP réel |
| État en mémoire | PostgreSQL ou Redis |
| Trace JSON locale | Observabilité distribuée |
| Reviewer simple | Évaluations automatisées |
| Validation manuelle booléenne | Workflow human-in-the-loop |

## 12. Message clé

Un projet multi-agent professionnel n’est pas une conversation entre plusieurs personnages.

C’est un système logiciel orchestré, testé, observable et contraint.
