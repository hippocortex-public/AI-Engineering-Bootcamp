# Corrigé — Exercices

## Objectif

Ce fichier contient les éléments de correction attendus pour les exercices du jour 04.  
Il est local à la journée afin de respecter la structure du bootcamp.

## Correction guidée

### 1. Lecture de l’énoncé

Avant d’implémenter une solution, vérifier systématiquement :

- les entrées attendues ;
- les sorties attendues ;
- les hypothèses implicites ;
- les cas limites ;
- les erreurs possibles.

### 2. Solution de référence

```python
from dataclasses import dataclass
from typing import Any


@dataclass
class ValidationResult:
    is_valid: bool
    message: str


def validate_payload(payload: dict[str, Any], required_fields: list[str]) -> ValidationResult:
    """Validate that a payload contains all required fields.

    This reference implementation is intentionally generic and executable.
    It can be adapted to the concrete exercise of the day.
    """
    missing_fields = [field for field in required_fields if field not in payload]

    if missing_fields:
        return ValidationResult(
            is_valid=False,
            message=f"Missing required fields: {', '.join(missing_fields)}",
        )

    return ValidationResult(is_valid=True, message="Payload is valid")


if __name__ == "__main__":
    sample_payload = {"prompt": "Explain embeddings", "model": "local-test-model"}
    result = validate_payload(sample_payload, ["prompt", "model"])
    print(result)
```

### 3. Points de contrôle

La solution est considérée correcte si elle :

- est exécutable sans dépendance externe non documentée ;
- expose clairement les hypothèses ;
- traite les cas d’erreur ;
- produit une sortie déterministe ;
- reste lisible et testable.

## Notes formateur

Adapter les détails de cette correction au contenu exact de `exercises.md` lorsque les exercices définitifs du jour 04 sont disponibles.  
Ne pas déplacer ce fichier : les corrections restent locales à chaque journée.
