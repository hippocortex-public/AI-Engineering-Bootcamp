# Notes formateur — Jour 2 — Coordination

## Intention pédagogique

Cette journée doit faire comprendre que le multi-agent est d'abord un problème d'architecture logicielle.  
Les apprenants doivent sortir de l'idée "plus d'agents = meilleur système".

Le message central est :

```text
La coordination est le produit.
```

## Points à insister

- Un agent spécialiste n'a pas la vision système.
- Le coordinateur doit rendre les décisions observables.
- Le routing est une décision.
- Le handoff est un transfert de contrôle.
- La revue est une politique, pas un agent magique.
- Le contexte doit être filtré.
- Les conflits doivent être visibles.

## Pièges fréquents

### Piège 1 — Appeler tous les agents

Les apprenants peuvent proposer d'appeler tous les agents à chaque demande.  
Corriger en parlant coût, bruit, latence et sécurité.

### Piège 2 — Faire confiance au reviewer sans critères

Un reviewer sans grille ne vaut pas mieux qu'une opinion supplémentaire.  
Demander toujours : "Qu'est-ce qui déclenche la revue ?"

### Piège 3 — Masquer les désaccords

Une belle synthèse qui cache un conflit est dangereuse.  
Le système doit exprimer l'incertitude.

### Piège 4 — Confondre state et trace

Le state représente l'état courant.  
La trace représente l'historique des décisions.

## Démonstration recommandée

Lancer :

```bash
python multi_agent_coordinator.py
python test_multi_agent_coordinator.py
```

Puis montrer :

- le plan ;
- les agents sélectionnés ;
- les observations ;
- la revue ;
- la trace JSON.

## Questions de discussion

- Quand faut-il préférer un handoff à un manager-worker ?
- Un reviewer doit-il être un LLM ou une règle déterministe ?
- Comment gérer une contradiction entre sécurité et produit ?
- Quelle trace serait nécessaire pour auditer une réponse client ?
- Comment brancher des outils MCP sans changer la politique de coordination ?

## Critère de maîtrise

Un apprenant maîtrise la journée s'il peut concevoir un workflow multi-agent avec :

- sélection contrôlée ;
- contexte minimal ;
- conflit explicite ;
- revue conditionnelle ;
- trace exploitable ;
- tests unitaires.
