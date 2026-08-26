# Corrigé — Challenge — Jour 7 — Projet multi-agent

## Approche proposée

L’extension consiste à ajouter un agent `qa` entre l’agent `engineer` et l’agent `reviewer`.

Le rôle de `qa` n’est pas de produire l’architecture. Il produit une stratégie de validation :

- tests fonctionnels ;
- tests d’intégration ;
- tests de non-régression ;
- tests de rollback ;
- critères de livraison.

## Nouvel outil

```python
def generate_release_checklist(release_name: str, risk_level: str) -> dict:
    return {
        "release_name": release_name,
        "risk_level": risk_level,
        "checks": [
            "documentation updated",
            "unit tests passed",
            "integration tests passed",
            "rollback plan validated",
            "security review completed",
        ],
    }
```

## Nouvel agent

```python
class QAAgent:
    role = "qa"

    def run(self, task, context, tools):
        checklist = tools.call(
            "generate_release_checklist",
            {"release_name": task.title, "risk_level": "medium"},
        )
        return Artifact(
            name="qa_release_checklist",
            kind="qa",
            content=checklist,
            created_by=self.role,
        )
```

## Tests à ajouter

- vérifier que l’agent `qa` est sélectionné pour une livraison ;
- vérifier que l’outil `generate_release_checklist` valide ses arguments ;
- vérifier qu’une action de déploiement est bloquée sans approbation ;
- vérifier que le reviewer voit l’artefact QA ;
- vérifier que la trace contient l’événement QA.

## Exemple de sortie JSON

```json
{
  "status": "completed",
  "artifacts": [
    "delivery_plan",
    "architecture_proposal",
    "qa_release_checklist",
    "security_review"
  ],
  "review": {
    "score": 0.9,
    "verdict": "approved"
  }
}
```

## Justification

L’ajout d’un agent QA est justifié parce que la qualité de livraison est une responsabilité stable, distincte de l’architecture et de la sécurité. L’outil de checklist reste borné et testable, tandis que l’agent QA interprète le contexte du projet pour produire une validation adaptée.
