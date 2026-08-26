# Exercices — Jour 6

## Exercice 1 — Identifier les composants d'une boucle

Pour chacun des éléments suivants, indique s'il s'agit d'un `goal`, d'un `state`, d'un `plan`, d'une `action`, d'une `observation` ou d'une `final answer`.

1. `lookup_order({"order_id": "A-100"})`
2. `status=delayed, eta=2026-09-02`
3. `Préparer une réponse pour un client dont la commande est en retard`
4. `order_id=A-100, missing_facts=[]`
5. `Récupérer l'état de la commande puis rédiger une réponse`
6. `Bonjour, votre commande est retardée et devrait arriver le 2 septembre.`

## Exercice 2 — Condition d'arrêt

On vous donne cette boucle :

```python
while True:
    action = choose_action(state)
    observation = execute(action)
    state = update(state, observation)
```

Listez au moins quatre problèmes d'engineering.

Puis proposez une version améliorée en pseudo-code.

## Exercice 3 — Replanification

Un agent commence avec ce plan :

```text
1. Extraire l'identifiant de commande.
2. Appeler lookup_order.
3. Rédiger la réponse client.
```

Mais le message utilisateur est :

```text
Ma commande est en retard, pouvez-vous m'aider ?
```

Expliquez pourquoi le plan ne peut pas continuer tel quel.

Proposez une étape de replanification.

## Exercice 4 — Journal d'exécution

Écrivez un exemple de trace JSON pour une itération d'agent qui appelle l'outil `lookup_order`.

La trace doit contenir :

- le numéro d'itération ;
- le nom de l'action ;
- les arguments ;
- le succès ou l'échec ;
- les champs d'état mis à jour.

## Exercice 5 — Implémentation guidée

Dans le lab, ouvrez `agent_loop_planner.py`.

Complétez mentalement le rôle de chaque classe :

- `AgentState`
- `PlanStep`
- `ToolAction`
- `Observation`
- `ToolRegistry`
- `AgentLoop`

Puis exécutez :

```bash
python agent_loop_planner.py
python test_agent_loop_planner.py
```

## Exercice 6 — Design critique

Vous rejoignez une équipe qui a implémenté un agent de support ainsi :

```python
def run_agent(user_message):
    prompt = "Tu es un agent autonome. Résous la demande."
    return call_llm(prompt + user_message)
```

Expliquez pourquoi ce système n'est pas un agent fiable pour la production.

Proposez une architecture en quatre composants.
