# Corrigé — Contrôler promotion et rollback

## Décision

La readiness prouve la capacité à servir les dépendances, puis les smoke tests
vérifient les chemins fonctionnels importants. La récupération doit être vérifiée
avec les mêmes contrôles. Une compatibilité de schéma inconnue bloque la livraison.

## Implémentation exécutable

Ce code correspond à `labs/rollout_solution.py`. Les callbacks ne lancent aucun
conteneur ; ils simulent les décisions que la procédure manuelle doit prendre.

```python
"""Corrigé de décision : callbacks simulés, aucune commande Docker exécutée ici."""
from dataclasses import dataclass


class RolloutFailed(Exception):
    pass


@dataclass(frozen=True)
class RolloutResult:
    active_release: str
    rolled_back: bool


def rollout(previous, candidate, deploy, readiness, smoke, schema_compatible=True):
    if not previous or not candidate or previous == candidate:
        raise ValueError("Distinct previous and candidate releases are required")
    if not schema_compatible:
        raise ValueError("Schema is incompatible with rollback")
    try:
        # Le callback deploy doit contenir son propre délai maximal.
        deploy(candidate)
        if not readiness() or not smoke():
            raise RolloutFailed("Candidate failed release checks")
        return RolloutResult(candidate, False)
    except Exception:
        try:
            deploy(previous)
            if not readiness() or not smoke():
                raise RolloutFailed("Previous release failed recovery checks")
        except Exception:
            raise RolloutFailed("Rollback failed; manual recovery required") from None
        return RolloutResult(previous, True)
```

## Démonstration d'un échec de candidate

```python
deployed = []
smoke_results = iter([False, True])
result = rollout(
    "release-001", "release-002", deployed.append,
    lambda: True, lambda: next(smoke_results), schema_compatible=True,
)
assert deployed == ["release-002", "release-001"]
assert result.active_release == "release-001" and result.rolled_back
print("Candidate refusée ; précédente revalidée")
```

## Adapter les callbacks

`deploy` doit exécuter l'application de l'image exacte, attendre avec un délai maximal
et conserver stdout/stderr sans secrets. Un code de retour non nul lève une erreur.
`readiness` effectue des sondes bornées ; `smoke` exécute les scénarios avec une identité
de test. Une attente infinie à l'intérieur d'un callback empêcherait le contrôleur
de lancer sa récupération.

La version précédente doit être disponible avant mutation. Prévoir l'exclusion
mutuelle de deux pipelines sur le même environnement et vérifier le digest actif.
Ne pas utiliser un booléen fabriqué pour contourner une incompatibilité de migration.
La compatibilité relève du contrat de schéma et de la stratégie expand/contract.

## Limites

Le contrôleur ne restaure ni DB ni configuration de secrets, ne journalise pas un
historique de release et ne garantit pas de bascule sans interruption. Une erreur
peut survenir après une mutation partielle ; sa récupération exige l'idempotence
des callbacks. Les tests prouvent le contrat de décision, pas un déploiement Docker.
