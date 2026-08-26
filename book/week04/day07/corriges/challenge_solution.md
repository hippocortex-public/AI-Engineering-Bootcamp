# Corrigé — Challenge

Une solution acceptable consiste à créer une méthode de façade qui assemble les composants existants.

Exemple de structure :

```python
def run_support_case(framework, user_id, message, approval=False):
    framework.memory.remember(
        user_id=user_id,
        key="preferred_tone",
        value="professionnel et empathique"
    )

    result = framework.run(
        user_id=user_id,
        message=message,
        workflow_name="support_resolution",
        approval=approval
    )

    return {
        "status": result.status,
        "summary": result.summary,
        "outputs": result.outputs,
        "blocked_actions": result.blocked_actions,
        "trace": result.trace,
        "memory_used": result.memory_used,
    }
```

Le workflow peut contenir :

```text
classify_ticket
search_kb
risk_review
draft_answer
prepare_refund
```

`prepare_refund` doit être sensible. Sans approbation, il doit être bloqué et non exécuté.

## Points importants

- Le statut final peut être `blocked` si une action sensible est requise.
- Le résultat peut rester utile même avec une action bloquée.
- La trace doit rendre le blocage explicite.
- Le système doit distinguer rédaction de réponse et exécution réelle du remboursement.

## Exemple de sortie

```json
{
  "status": "blocked",
  "summary": "Réponse préparée, remboursement bloqué sans approbation.",
  "outputs": {
    "category": "refund_request",
    "draft": "Nous sommes désolés..."
  },
  "blocked_actions": ["issue_refund"],
  "memory_used": ["preferred_tone"]
}
```
