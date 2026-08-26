# Corrigé — Exercices

## Exercice 1 — Identifier le type de système

1. Chatbot simple.
   - Type : génération textuelle.
   - Risque : faible à moyen selon le domaine.
   - Condition d'arrêt : réponse produite.

2. Assistant outillé.
   - Type : assistant avec function calling.
   - Risque : dépend de l'outil.
   - Condition d'arrêt : réponse produite après appel d'outil ou sans appel.

3. Agent autonome.
   - Type : agent planifiant et exécutant plusieurs étapes.
   - Risque : moyen à élevé.
   - Condition d'arrêt : objectif atteint, clarification nécessaire, budget dépassé ou erreur.

4. Workflow automatisé.
   - Type : orchestration déterministe.
   - Risque : dépend des actions configurées.
   - Condition d'arrêt : fin du workflow ou erreur.

5. Agent autonome non contrôlé.
   - Type : agent à risque élevé.
   - Risque : élevé car action sensible automatique.
   - Condition d'arrêt attendue : approbation humaine obligatoire avant remboursement.

## Exercice 2 — Définir un état d'agent

Exemple :

```json
{
  "user_id": "user-123",
  "objective": "Réserver un restaurant pour deux personnes demain soir",
  "status": "needs_input",
  "collected_fields": {
    "party_size": 2,
    "date": "tomorrow",
    "meal": "dinner"
  },
  "missing_inputs": ["city", "time"],
  "tasks": [
    {
      "id": "T1",
      "name": "Collecter les champs manquants",
      "tool_name": "ask_user",
      "status": "pending"
    }
  ],
  "traces": [
    {
      "step": 0,
      "event_type": "clarification_required",
      "message": "City and time are missing"
    }
  ],
  "final_answer": null
}
```

## Exercice 3 — Écrire un plan

Plan possible :

```json
[
  {
    "id": "T1",
    "name": "Vérifier la commande",
    "tool_name": "check_order",
    "sensitive": false,
    "status": "pending"
  },
  {
    "id": "T2",
    "name": "Vérifier si la commande est encore modifiable",
    "tool_name": "check_delivery_policy",
    "sensitive": false,
    "status": "pending"
  },
  {
    "id": "T3",
    "name": "Valider la nouvelle adresse avec l'utilisateur",
    "tool_name": "ask_user_confirmation",
    "sensitive": false,
    "status": "pending"
  },
  {
    "id": "T4",
    "name": "Modifier l'adresse de livraison",
    "tool_name": "update_delivery_address",
    "sensitive": true,
    "status": "pending"
  },
  {
    "id": "T5",
    "name": "Rédiger la réponse finale",
    "tool_name": "draft_response",
    "sensitive": false,
    "status": "pending"
  }
]
```

## Exercice 4 — Ajouter un garde-fou

La règle :

```python
if state.budget_used + expected_cost > state.max_budget:
    stop()
```

est plus stricte que :

```python
if state.budget_used >= state.max_budget:
    stop()
```

car elle empêche de dépasser le budget avant l'exécution du prochain outil.

La deuxième règle ne bloque qu'une fois le budget déjà atteint. Elle peut donc autoriser une action qui fera dépasser la limite.

## Exercice 5 — Tester une action sensible

Exemple :

```python
def test_sensitive_tool_requires_approval():
    agent = make_agent()
    state = agent.start("u1", "Je veux un remboursement pour ORDER-1234")
    final_state = agent.run(state, approve_sensitive_actions=False)

    assert final_state.status == RunStatus.NEEDS_INPUT
    assert "approval_for_issue_refund" in final_state.missing_inputs
    assert any(task.status == TaskStatus.BLOCKED for task in final_state.tasks)
    assert any(event.event_type == "approval_required" for event in final_state.traces)
```

## Exercice 6 — Reprise d'exécution

`to_json()` permet de sauvegarder l'état complet du run :

```python
payload = state.to_json()
```

`from_json()` permet de reconstruire cet état :

```python
restored_state = AgentState.from_json(payload)
```

Cette capacité est utile lorsqu'un agent demande une validation humaine.

Exemple :

1. l'agent prépare un remboursement ;
2. il s'arrête avec `needs_input` ;
3. l'état est stocké en base ;
4. un humain valide ;
5. l'état est rechargé ;
6. l'exécution reprend.
