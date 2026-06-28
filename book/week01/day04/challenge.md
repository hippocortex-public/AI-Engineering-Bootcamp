# Challenge — Construire un estimateur de contexte

## Objectif

Construire un petit outil Python qui estime si un prompt peut entrer dans une fenêtre de contexte donnée.

## Contexte

Vous développez un backend IA qui assemble :

- une instruction système ;
- un historique conversationnel ;
- des documents récupérés ;
- une question utilisateur ;
- une réponse attendue.

Avant d’appeler le modèle, le backend doit refuser ou réduire le contexte si le budget est dépassé.

## Travail demandé

Créer une fonction :

```python
def build_context_plan(
    context_window: int,
    reserved_output_tokens: int,
    sections: dict[str, str],
    chars_per_token: float = 4.0,
) -> dict:
    ...
```

La fonction doit retourner :

```python
{
    "context_window": 16000,
    "reserved_output_tokens": 1500,
    "estimated_input_tokens": 12000,
    "remaining_tokens": 2500,
    "fits": True,
    "sections": {
        "system": 120,
        "history": 4000,
        "documents": 7600,
        "question": 280
    },
    "recommendations": []
}
```

## Contraintes

- Ne pas utiliser de dépendance externe.
- Fournir une estimation simple basée sur `chars_per_token`.
- Ajouter au moins trois recommandations si le budget est dépassé.
- Prévoir des erreurs explicites si les paramètres sont invalides.
- Ajouter un exemple d’exécution.

## Critères de réussite

- Le code s’exécute avec Python standard.
- Les valeurs invalides sont gérées.
- Le résultat est lisible.
- La logique est testable.
- Les recommandations sont orientées production.
