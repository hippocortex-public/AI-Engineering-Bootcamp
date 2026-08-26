# Corrigé — Challenge — Coordinateur multi-agent contrôlé

## Approche recommandée

Une bonne solution consiste à séparer cinq responsabilités :

1. `AgentRegistry` : connaît les agents disponibles.
2. `CoordinationPolicy` : décide des règles de revue et de conflit.
3. `MultiAgentCoordinator` : orchestre le workflow.
4. `SpecialistAgent` : produit une observation locale.
5. `CoordinationResult` : expose une sortie structurée.

## Exemple de politique

```python
def needs_review(task, selected_agents, conflicts, sensitive_action):
    return (
        task.risk_level == "high"
        or bool(conflicts)
        or "security_agent" in selected_agents
        or sensitive_action
        or not selected_agents
    )
```

## Gestion du contexte minimal

Chaque agent reçoit une vue filtrée :

```python
{
    "task_id": task.task_id,
    "objective": task.objective,
    "domains": matching_domains,
    "risk_level": task.risk_level,
    "constraints": task.constraints,
}
```

## Sortie attendue

La sortie doit être sérialisable :

```python
result.to_dict()
```

Exemple :

```json
{
  "task_id": "task-001",
  "status": "needs_review",
  "selected_agents": ["support_agent", "security_agent"],
  "review_performed": true,
  "conflicts": [],
  "final_answer": "Review completed. Security constraints must be respected.",
  "trace": [
    {"type": "task_received", "task_id": "task-001"},
    {"type": "agents_selected", "agents": ["support_agent", "security_agent"]},
    {"type": "review_performed", "agent": "reviewer_agent"}
  ]
}
```

## Critères de validation

La solution est correcte si :

- les agents sont sélectionnés à partir des domaines ;
- le reviewer est déclenché selon les règles ;
- la trace explique les décisions ;
- les conflits ne sont pas masqués ;
- la sortie est déterministe ;
- les tests passent sans dépendance externe.

## Extension quorum

Une implémentation simple :

```python
statuses = [observation.status for observation in observations]
most_common_status = max(set(statuses), key=statuses.count)

if len(observations) >= 3 and statuses.count(most_common_status) >= 2:
    confidence = "medium"
else:
    confidence = "low"

if "blocked" in statuses:
    confidence = "low"
```

La règle de quorum ne doit jamais contourner un blocage sécurité ou une revue obligatoire.
