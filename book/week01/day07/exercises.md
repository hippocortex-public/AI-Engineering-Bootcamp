# Exercices — Premier client Python

## Exercice 1 — Identifier les responsabilités

Lis le pseudo-code suivant :

```python
def ask(prompt):
    from openai import OpenAI
    client = OpenAI(api_key="secret")
    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )
    print(response.output_text)
```

Réponds :

1. Quelles responsabilités sont mélangées ?
2. Pourquoi ce code est difficile à tester ?
3. Que faudrait-il extraire dans un client dédié ?

## Exercice 2 — Configuration

Écris une dataclass `LLMConfig` contenant :

- `model`;
- `temperature`;
- `max_output_tokens`;
- `timeout_seconds`;
- `api_key`.

Ajoute une méthode `from_env()` qui lit `OPENAI_API_KEY`.

## Exercice 3 — Transport mock

Implémente un transport mock avec une méthode `send(request)` qui retourne toujours :

```json
{
  "text": "Réponse mock",
  "model": "mock-model"
}
```

## Exercice 4 — Client minimal

Implémente une classe `LLMClient` avec une méthode :

```python
generate_text(prompt: str) -> LLMResponse
```

La méthode doit :

1. créer une requête ;
2. appeler le transport ;
3. retourner une réponse typée.

## Exercice 5 — Sortie JSON

Ajoute une méthode `generate_json(prompt, required_fields)` qui :

1. appelle `generate_text`;
2. parse le texte comme JSON ;
3. vérifie les champs obligatoires ;
4. lève une erreur si la sortie est invalide.

## Exercice 6 — Testabilité

Écris deux tests :

1. le client retourne une réponse mock ;
2. `generate_json` échoue si un champ obligatoire manque.

## Exercice 7 — Architecture

Dessine un diagramme Mermaid montrant :

- application ;
- client LLM ;
- configuration ;
- transport mock ;
- transport réel ;
- API externe.
