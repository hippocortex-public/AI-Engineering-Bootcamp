# Interview — Architecture d'un framework d'agents

## Questions

### Question 1

Pourquoi est-il dangereux de commencer un framework d'agents par une classe `Agent` qui fait tout ?

### Question 2

Quelle différence fais-tu entre `AgentDefinition` et `Runner` ?

### Question 3

Pourquoi le `ToolRegistry` doit-il être séparé du runner ?

### Question 4

Pourquoi faut-il définir une interface `ModelClient` au lieu d'appeler directement un SDK fournisseur partout dans le code ?

### Question 5

Qu'est-ce qu'un invariant d'architecture ? Donne un exemple dans un framework d'agents.

### Question 6

Quels signaux indiquent qu'une architecture agentique est trop couplée ?

### Question 7

Pourquoi l'observabilité doit-elle être prévue dès le début ?

### Question 8

Comment préparer l'intégration MCP sans rendre tout le framework dépendant de MCP ?

### Question 9

Quel composant devrait porter les limites d'itérations et les conditions d'arrêt ?

### Question 10

Comment tester l'architecture d'un framework sans appeler un vrai modèle ?
