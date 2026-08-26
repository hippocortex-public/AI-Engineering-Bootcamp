# Corrigé — Challenge

## Implémentation attendue

```python
from agent_abstraction import Agent, EchoModelClient, RunContext

client = EchoModelClient(
    canned_response=(
        "Un agent est une unité qui raisonne ou répond sur une tâche. "
        "Un workflow organise plusieurs étapes ou agents. "
        "Exemple : un agent support répond au client, tandis qu'un workflow "
        "peut router, enrichir, relire puis envoyer la réponse."
    )
)

agent = Agent(
    name="explainer",
    instructions="Explique simplement les concepts AI Engineering avec un exemple concret.",
    model_client=client,
    model="fake-model"
)

result = agent.run(
    RunContext(
        user_input="Explique la différence entre agent et workflow.",
        session_id="s-challenge",
        user_id="u-learner",
        metadata={"exercise": "challenge"}
    )
)

assert result.status == "completed"
assert result.agent_name == "explainer"
assert "agent" in result.output.lower()
assert "workflow" in result.output.lower()
assert result.trace
```

## Points de correction

Le challenge est correct si :

- le client modèle est injecté ;
- aucun SDK externe n’est appelé ;
- l’entrée utilise `RunContext` ;
- la sortie est un `AgentResult` ;
- la trace contient au moins la validation, la construction du prompt et l’appel modèle ;
- le résultat est déterministe.

## Extension reviewer

L’extension peut être simulée ainsi :

```python
reviewer = Agent(
    name="reviewer",
    instructions="Relis la réponse et vérifie qu'elle contient un exemple.",
    model_client=EchoModelClient("La réponse est claire et contient un exemple."),
    model="fake-model"
)

review = reviewer.run(
    RunContext(
        user_input=result.output,
        session_id="s-challenge",
        user_id="u-learner"
    )
)
```

Cela reste une composition manuelle, pas encore un workflow engine.
