# Lab — Modern API Patterns

## Objectif

Implémenter et tester localement les trois patterns du jour :

1. requête de type Responses API ;
2. Structured Outputs ;
3. Tool Calling.

## Fichiers utilisés

- `examples/week01/day06/modern_api_patterns.py`
- `tests/week01/day06/test_modern_api_patterns.py`

## Étape 1 — Explorer la requête support

Ouvrir le fichier Python et identifier :

- la classe `Message` ;
- la classe `ResponseRequest` ;
- la fonction `build_support_request`.

Exécuter :

```bash
python - <<'PY'
from examples.week01.day06.modern_api_patterns import build_support_request

request = build_support_request("Urgent production API timeout blocks checkout.")
print(request.to_payload())
PY
```

## Étape 2 — Tester la sortie structurée

Exécuter :

```bash
python - <<'PY'
from examples.week01.day06.modern_api_patterns import classify_support_ticket

print(classify_support_ticket("Urgent production API timeout blocks checkout."))
print(classify_support_ticket("I was charged twice for my invoice."))
PY
```

Observer :

- la catégorie ;
- la priorité ;
- le résumé.

## Étape 3 — Tester la validation

Exécuter :

```bash
python - <<'PY'
from examples.week01.day06.modern_api_patterns import validate_ticket_payload

try:
    validate_ticket_payload({
        "category": "technical",
        "priority": "urgent",
        "summary": "API timeout blocks checkout."
    })
except ValueError as exc:
    print("Rejected:", exc)
PY
```

## Étape 4 — Tester un Tool Call

Exécuter :

```bash
python - <<'PY'
from examples.week01.day06.modern_api_patterns import (
    ToolRegistry,
    execute_model_tool_call,
    get_order_status,
)

registry = ToolRegistry()
registry.register("get_order_status", get_order_status)

raw_tool_call = '{"name":"get_order_status","arguments":{"order_id":"A100"}}'
print(execute_model_tool_call(raw_tool_call, registry))
PY
```

## Étape 5 — Lancer les tests

Depuis la racine du livrable :

```bash
python -m pytest tests/week01/day06
```

Résultat attendu :

```text
5 passed
```

## Questions de lab

1. Pourquoi le registre refuse-t-il les outils inconnus ?
2. Pourquoi `arguments` doit-il être un objet ?
3. Quelle validation manque encore pour un vrai système de production ?
4. Où ajouteriez-vous des logs ?
5. Comment brancheriez-vous ce code sur une vraie API au Jour 7 ?

## Corrigé synthétique

1. Pour éviter qu'une sortie modèle appelle une fonction non autorisée.
2. Pour empêcher des formats imprévisibles et forcer un contrat.
3. Authentification, autorisation, validation métier, rate limiting, idempotence, audit.
4. À la construction de requête, au retour modèle, avant l'appel outil, après l'appel outil et en cas d'erreur.
5. En remplaçant les fonctions mockées par un client fournisseur tout en conservant les validations et les tests unitaires.
