# Corrigé — Interview

## Question 1

Une classe `Agent` qui fait tout mélange définition, exécution, outils, mémoire, sécurité et observabilité. Elle devient difficile à tester, à remplacer et à étendre. Chaque évolution touche le même bloc de code, ce qui augmente le risque de régression.

## Question 2

`AgentDefinition` décrit un agent : nom, instructions, outils autorisés, format de sortie, politiques. `Runner` exécute un agent : il gère les tours, les appels modèle, les appels outils, l'état, les traces et les conditions d'arrêt.

## Question 3

Le `ToolRegistry` doit être séparé pour éviter que chaque runner ou agent redéclare les outils. Cela permet aussi de centraliser validation, documentation, permissions et tests.

## Question 4

Une interface `ModelClient` rend le fournisseur de modèle remplaçable. Le framework peut être testé avec un faux client et évoluer sans réécrire toute l'orchestration.

## Question 5

Un invariant est une règle d'architecture qui doit toujours rester vraie. Exemple : `Observability` peut lire les événements d'exécution, mais ne doit jamais modifier l'état métier.

## Question 6

Signaux de couplage :

- une classe connaît tous les détails ;
- les outils importent le runner ;
- la mémoire appelle directement le modèle ;
- les tests nécessitent une vraie API ;
- ajouter un agent oblige à copier du code ;
- les logs contiennent de la logique métier.

## Question 7

L'observabilité doit être prévue dès le début, car les agents sont non déterministes et multi-étapes. Sans trace, il devient difficile de comprendre pourquoi un outil a été appelé ou pourquoi une réponse a été produite.

## Question 8

Il faut préparer MCP comme une intégration possible derrière un port. Le framework peut définir un `ToolProvider` ou un adaptateur MCP sans rendre le runner dépendant directement du protocole.

## Question 9

Les limites d'itérations et conditions d'arrêt appartiennent au `WorkflowEngine` ou à une `ExecutionPolicy` utilisée par le runner.

## Question 10

On peut tester avec :

- un faux `ModelClient`;
- des outils déterministes ;
- une mémoire en mémoire ;
- des traces capturées localement ;
- des tests d'invariants d'architecture ;
- des scénarios JSON.
