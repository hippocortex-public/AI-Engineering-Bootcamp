# Corrigé — Exercices Structured Outputs

## Exercice 1 — Identifier la bonne stratégie

### Cas A

Mécanisme adapté : **texte libre**.

Justification : l’utilisateur demande une explication pédagogique. La valeur principale est la clarté du raisonnement, pas une donnée machine consommée par un backend.

### Cas B

Mécanisme adapté : **function calling**.

Justification : le modèle doit sélectionner une fonction et fournir des arguments. La responsabilité principale est l’action externe.

### Cas C

Mécanisme adapté : **Structured Outputs**.

Justification : le backend consomme une décision métier typée. Il faut garantir la présence de `category`, `priority` et `owner_team`.

### Cas D

Mécanisme adapté : **JSON mode** ou JSON libre encadré.

Justification : pour un prototype non critique, produire un JSON syntaxiquement valide peut suffire. En production, il faudrait passer à un schéma strict.

## Exercice 2 — Concevoir un schéma

Exemple de schéma correct :

```json
{
  "type": "object",
  "required": ["intent", "requires_tool", "missing_fields", "confidence"],
  "additionalProperties": false,
  "properties": {
    "intent": {
      "type": "string",
      "enum": ["order_status", "refund", "technical_issue", "other"]
    },
    "requires_tool": {
      "type": "boolean"
    },
    "missing_fields": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    }
  }
}
```

## Exercice 3 — Détecter les erreurs

Sortie fournie :

```json
{
  "category": "finance",
  "priority": "urgent",
  "confidence": "0.9",
  "explanation": "Client très mécontent"
}
```

Erreurs :

1. `category` vaut `finance`, qui n’est pas dans l’enum autorisée.
2. `priority` vaut `urgent`, qui n’est pas dans l’enum autorisée.
3. `confidence` est une chaîne alors que le contrat attend un nombre.
4. `explanation` est une propriété supplémentaire non prévue.
5. Si le schéma impose `additionalProperties: false`, la sortie doit être rejetée.
6. Selon le schéma complet du jour, d’autres champs obligatoires manqueraient aussi : `sentiment`, `summary`, `action_required`, `next_action`.

## Exercice 4 — Mapper vers un objet métier

Objet métier possible :

```python
@dataclass(frozen=True)
class TriageDecision:
    category: str
    priority: str
    sentiment: str
    summary: str
    action_required: bool
    owner_team: str
    rationale: str
    confidence: float
```

Avant instanciation, il faut valider :

- la présence de tous les champs ;
- les types ;
- les enums ;
- la borne de `confidence` ;
- la présence de `next_action.owner_team` ;
- la présence de `next_action.rationale` ;
- l’absence de propriétés inattendues.

## Exercice 5 — Stratégie de récupération

Stratégie robuste :

1. Journaliser l’erreur :
   - identifiant de requête ;
   - schéma attendu ;
   - champ manquant ;
   - sortie brute ;
   - modèle utilisé si disponible.
2. Redemander au modèle une sortie strictement conforme au même schéma.
3. Si la deuxième tentative échoue :
   - router vers `support_l1` ;
   - marquer la décision comme non automatisée ;
   - demander une revue humaine si l’impact est élevé.
4. Ne pas inventer une confiance par défaut sans le signaler, car cela crée une fausse certitude et masque un défaut de qualité du système.
