# Corrigé — Challenge Function Calling

## Solution de référence

La solution de référence est disponible dans :

```text
book/week02/day02/labs/function_calling_agent.py
```

Elle contient :

- les schémas d’outils ;
- la classe `ToolRegistry` ;
- la classe `SupportAgent`;
- un planificateur simulé ;
- des erreurs structurées ;
- des traces d’observabilité.

Les tests sont disponibles dans :

```text
book/week02/day02/labs/test_function_calling_agent.py
```

## Extrait principal

```python
registry = build_registry()
agent = SupportAgent(registry=registry, planner=FakePlanner())

response = agent.run("Quel est le statut de la commande ORD-1001 ?")
print(response)
```

Sortie attendue simplifiée :

```python
{
    "ok": True,
    "message": "La commande ORD-1001 est shipped.",
    "tool_result": {
        "order_id": "ORD-1001",
        "status": "shipped",
        "carrier": "DHL"
    }
}
```

## Décisions côté application

L’application contrôle :

- la liste réelle des outils disponibles ;
- les règles de validation ;
- les permissions ;
- le dispatch ;
- les logs ;
- les confirmations ;
- la gestion d’erreurs.

## Décisions laissées au modèle

Le modèle peut décider :

- quel outil semble pertinent ;
- quels arguments extraire du message ;
- comment formuler une réponse finale à partir du résultat.

## Protections

La solution protège l’exécution par :

- un registre explicite ;
- une validation stricte des arguments ;
- le refus des outils inconnus ;
- le refus des arguments supplémentaires ;
- le refus des valeurs hors enum ;
- l’absence de `eval`, `exec` et `globals()`.
