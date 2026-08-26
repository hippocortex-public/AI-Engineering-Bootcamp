# Corrigé — Exercices

## Exercice 1 — Identifier les responsabilités

| Responsabilité | Catégorie |
|---|---|
| Construire le prompt système | Agent |
| Exécuter une requête HTTP vers le fournisseur LLM | ModelClient |
| Valider que l’entrée utilisateur n’est pas vide | Agent |
| Choisir le prochain nœud d’un workflow | Runner / Workflow |
| Retourner un `AgentResult` | Agent |
| Persister une mémoire long terme | Memory Layer |
| Injecter un faux modèle pour les tests | Test / Infrastructure |
| Appliquer une limite de longueur d’entrée | Agent |

Le point clé est de garder l’agent responsable de son contrat d’exécution, mais pas des détails fournisseur ni de l’orchestration globale.

## Exercice 2 — Concevoir un contrat

Exemple :

```python
from dataclasses import dataclass, field

@dataclass
class RunContext:
    user_input: str
    session_id: str
    user_id: str
    metadata: dict = field(default_factory=dict)
```

Cette structure est minimale, explicite et sérialisable si `metadata` contient seulement des types JSON.

## Exercice 3 — Standardiser une sortie

```python
{
    "agent_name": "support_agent",
    "status": "completed",
    "output": "Votre ticket est prioritaire.",
    "usage": {
        "input_chars": 34,
        "output_chars": 29
    },
    "trace": [
        {
            "step": "model_call",
            "message": "Model client completed successfully."
        }
    ]
}
```

Une sortie structurée permet l’orchestration, la supervision, les tests et le debug.

## Exercice 4 — Repérer les anti-patterns

Problèmes :

1. le SDK fournisseur est importé dans la méthode métier ;
2. l’agent n’est pas testable sans clé API ;
3. aucun contrat de sortie structuré ;
4. aucune trace ;
5. aucune validation de l’entrée ;
6. aucun statut d’exécution ;
7. le prompt est construit de manière implicite ;
8. le modèle est codé en dur.

Une version framework doit injecter un `ModelClient` et retourner un `AgentResult`.

## Exercice 5 — Modifier le lab

Exemple de stratégie :

```python
if "DROP TABLE" in context.user_input.upper():
    return AgentResult(
        agent_name=self.name,
        output="",
        status="blocked",
        usage={"input_chars": len(context.user_input), "output_chars": 0},
        trace=[
            TraceEvent(step="guardrail", message="Unsafe database instruction blocked.").to_dict()
        ],
    )
```

Le plus important : le modèle ne doit pas être appelé.

## Exercice 6 — Préparer l’extension tools

Modification minimale :

```python
from dataclasses import field

@dataclass
class Agent:
    name: str
    instructions: str
    model_client: ModelClient
    model: str = "fake-model"
    tools: list[str] = field(default_factory=list)
```

À ce stade, `tools` peut rester descriptif. Le comportement réel viendra au jour 3 avec `Tool Registry`.
