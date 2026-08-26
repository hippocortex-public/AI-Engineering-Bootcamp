# Review formateur — Semaine 4 Jour 1

## Points à vérifier

- L'apprenant distingue définition d'agent et exécution.
- L'apprenant sait expliquer pourquoi le runner ne doit pas contenir toute la logique.
- Les responsabilités sont réparties sans chevauchement majeur.
- Les dépendances ne forment pas de cycle.
- Les invariants sont vérifiables.
- Le diagramme Mermaid reflète l'architecture écrite.
- Le code du lab est exécuté et les tests passent.

## Erreurs fréquentes

### 1. Créer une classe `Agent` omnisciente

Symptôme :

```python
class Agent:
    def call_model(self): ...
    def call_tool(self): ...
    def save_memory(self): ...
    def log(self): ...
    def validate_security(self): ...
```

Correction : distinguer `AgentDefinition`, `Runner`, `ToolRegistry`, `MemoryStore` et `Observability`.

### 2. Faire dépendre les outils du runner

Un outil doit exécuter une action métier ou technique. Il ne doit pas connaître la boucle agentique.

### 3. Oublier les traces

Les traces ne sont pas un détail de production. Elles sont nécessaires dès les tests pour comprendre les décisions de l'agent.

### 4. Confondre mémoire et état

L'état décrit une tâche en cours. La mémoire peut survivre à plusieurs sessions. Les deux doivent rester explicites.

## Questions de validation orale

- Où placerais-tu une validation humaine avant suppression de données ?
- Comment ajouterais-tu un second fournisseur de modèle ?
- Comment testerais-tu le runner sans modèle réel ?
- Quel composant devrait exposer des outils MCP ?
- Que se passe-t-il si deux composants dépendent mutuellement l'un de l'autre ?

## Critère de passage au jour 2

L'apprenant peut passer au jour 2 s'il est capable de dessiner l'architecture du mini-framework et d'expliquer la responsabilité de chaque composant sans utiliser une classe unique qui fait tout.
