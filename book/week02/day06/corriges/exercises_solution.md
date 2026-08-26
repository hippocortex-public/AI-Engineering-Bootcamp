# Corrigé — Exercices — Jour 6

## Corrigé exercice 1

1. `lookup_order({"order_id": "A-100"})` : action.
2. `status=delayed, eta=2026-09-02` : observation.
3. `Préparer une réponse pour un client dont la commande est en retard` : goal.
4. `order_id=A-100, missing_facts=[]` : state.
5. `Récupérer l'état de la commande puis rédiger une réponse` : plan.
6. `Bonjour, votre commande est retardée et devrait arriver le 2 septembre.` : final answer.

## Corrigé exercice 2

Problèmes :

- boucle infinie possible ;
- absence de limite d'itérations ;
- absence de condition d'arrêt ;
- absence de gestion d'erreur ;
- absence de journalisation ;
- action non validée ;
- outil inconnu possible ;
- aucune distinction entre observation et final answer.

Pseudo-code amélioré :

```python
state = initialize_state(goal)
max_iterations = 5

while not state.done and state.iterations < max_iterations:
    action = choose_action(state)

    if not registry.has_tool(action.tool_name):
        state.status = "error"
        break

    observation = registry.execute(action)
    state = reducer.apply(state, action, observation)

    if should_finish(state):
        state.status = "completed"
        state.done = True

if not state.done and state.iterations >= max_iterations:
    state.status = "max_iterations_reached"
```

## Corrigé exercice 3

Le plan ne peut pas continuer car l'étape `lookup_order` nécessite un `order_id`.

Le message utilisateur ne contient aucun identifiant exploitable. L'agent ne doit pas inventer de valeur.

Replanification :

```text
1. Demander à l'utilisateur son identifiant de commande.
2. Mettre le statut à waiting_for_user.
3. Suspendre la boucle.
```

## Corrigé exercice 4

Exemple :

```json
{
  "iteration": 1,
  "action": "lookup_order",
  "arguments": {
    "order_id": "A-100"
  },
  "success": true,
  "updated_fields": ["order_status", "eta"]
}
```

## Corrigé exercice 5

Rôles :

- `AgentState` : état courant de résolution.
- `PlanStep` : étape de planification.
- `ToolAction` : action concrète à exécuter.
- `Observation` : résultat d'une action.
- `ToolRegistry` : registre contrôlé des outils autorisés.
- `AgentLoop` : orchestration de la boucle complète.

## Corrigé exercice 6

Le système proposé n'est pas fiable car il délègue toute l'architecture au prompt.

Il manque :

- un état explicite ;
- une liste d'outils autorisés ;
- une validation des arguments ;
- une condition d'arrêt ;
- une trace d'exécution ;
- une gestion d'erreur ;
- une limite d'itérations.

Architecture proposée :

```text
Planner -> Policy -> ToolRegistry -> Reducer
```

- `Planner` produit le plan.
- `Policy` choisit l'action suivante.
- `ToolRegistry` exécute uniquement les outils autorisés.
- `Reducer` met à jour l'état avec les observations.
