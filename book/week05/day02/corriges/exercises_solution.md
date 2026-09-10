# Corrigé — Exercices

## Exercice 1

| Responsabilité | Catégorie | Explication |
|---|---|---|
| Lire `X-API-Key` | API HTTP | C'est une précondition d'accès au routeur protégé. |
| Classer l'intention | Service applicatif | C'est une décision métier ou agentique. |
| Retourner `401` | API HTTP | La route transforme une erreur d'accès en réponse HTTP. |
| Stocker un tour | Service applicatif | Le stockage de session appartient à l'état applicatif. |
| Valider la taille | API HTTP | La limite protège l'entrée avant traitement. |
| Générer la réponse | Service applicatif | La réponse dépend du domaine, pas du transport. |
| Renvoyer `X-Request-ID` | API HTTP | C'est une responsabilité de middleware. |
| Masquer les emails | Service applicatif | Dans le lab, la redaction est faite avant stockage métier. |

## Exercice 2

Le champ `channel` doit être validé dans le modèle Pydantic, par exemple avec un `Literal`.

Il ne doit pas rester une chaîne libre parce que :

- les dashboards deviendraient incohérents ;
- les clients pourraient envoyer des valeurs non prévues ;
- les règles métier par canal deviendraient fragiles.

Il aide l'observabilité en permettant de comparer les erreurs, latences et volumes par canal.

## Exercice 3

Exemple :

```json
{
  "error": "429",
  "message": "rate limit exceeded for session session-123",
  "request_id": "req-001",
  "limit": 5,
  "remaining": 0
}
```

## Exercice 4

`TestClient` est adapté parce qu'il exécute l'application FastAPI directement, sans serveur réseau externe.

Deux cas à tester en HTTP :

1. l'authentification par en-tête ;
2. la validation Pydantic et les codes d'erreur.

Ces comportements dépendent de FastAPI et ne sont pas visibles dans un simple test de fonction métier.

## Exercice 5

`ai_platform/__init__.py` est la façade publique du package.

Si le jour 2 remplace les exports du jour 1, le code suivant peut casser :

```python
from ai_platform import ArchitectureBlueprint
```

La construction du framework serait alors non cumulative, ce qui contredit la progression pédagogique de la semaine.
