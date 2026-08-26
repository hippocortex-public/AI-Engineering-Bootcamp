# Corrigé — Questions d’entretien

## 1. Quelle différence fais-tu entre un modèle de langage et un agent ?

Un modèle de langage produit une sortie à partir d’une entrée.

Un agent est une architecture logicielle autour du modèle. Il peut maintenir un état, décider d’une action, appeler des outils, lire des observations et produire une réponse finale.

## 2. Pourquoi un agent doit-il maintenir un état ?

L’état permet de conserver les informations utiles pendant l’exécution :

- demande utilisateur ;
- action choisie ;
- observations ;
- réponse finale ;
- trace.

Sans état explicite, le comportement devient difficile à inspecter et à tester.

## 3. Qu’est-ce qu’un outil dans une architecture agentique ?

Un outil est une fonction ou un service externe que l’agent peut appeler pour obtenir une information ou effectuer une action.

Exemples :

- rechercher une commande ;
- consulter un stock ;
- interroger une base de données ;
- appeler une API interne.

## 4. À quoi sert une trace d’exécution ?

La trace d’exécution permet de comprendre le chemin suivi par l’agent.

Elle aide à :

- déboguer ;
- auditer ;
- évaluer ;
- expliquer ;
- tester.

## 5. Quelle est la différence entre mémoire et état ?

L’état concerne l’exécution courante.

La mémoire désigne des informations conservées au-delà d’une seule exécution ou conversation.

Exemple :

- état : action choisie pour la demande actuelle ;
- mémoire : préférence utilisateur sauvegardée pour les prochaines sessions.

## 6. Pourquoi séparer la politique de décision de l’exécution des outils ?

La séparation permet de tester la décision sans déclencher d’effet externe.

Elle évite aussi qu’un outil sensible soit appelé par erreur à cause d’une logique difficile à isoler.

## 7. Quels risques apparaissent lorsqu’un agent peut appeler des outils externes ?

Risques principaux :

- appels non désirés ;
- effets irréversibles ;
- fuite de données ;
- coûts inattendus ;
- erreurs silencieuses ;
- dépendance à des services externes.

## 8. Pourquoi commencer par un agent mono-agent ?

Un agent mono-agent est plus simple à comprendre, tester et observer.

Il permet de maîtriser les fondamentaux avant d’introduire la coordination multi-agent, qui ajoute de la complexité.

## Question de raisonnement 1

Pour rendre le comportement testable, je séparerais :

- `decide_action` ;
- `lookup_order` ;
- `lookup_inventory` ;
- `run_agent` ;
- `AgentState`.

Ensuite, j’écrirais des tests par chemin :

- demande commande ;
- demande stock ;
- demande générale.

## Question de raisonnement 2

Il faut inspecter :

1. la politique de décision ;
2. les conditions de déclenchement de l’outil ;
3. les garde-fous avant appel ;
4. la trace d’exécution ;
5. les tests couvrant les cas sensibles.

## Question de raisonnement 3

J’ajouterais :

- une trace structurée ;
- des logs par étape ;
- un identifiant de requête ;
- l’action sélectionnée ;
- les entrées/sorties des outils non sensibles ;
- les erreurs ;
- la latence ;
- le statut final.
