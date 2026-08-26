# Corrigé — Challenge Structured Outputs

## Solution attendue

Une solution robuste sépare quatre étapes :

```text
raw output
→ json.loads
→ validate_schema
→ map_to_domain_object
→ business decision
```

## Exemple de code minimal

Le fichier `labs/structured_output_agent.py` fournit une implémentation complète sans dépendance externe.

Les éléments importants sont :

- `TRIAGE_OUTPUT_SCHEMA` : contrat de sortie ;
- `validate_schema` : validation stricte ;
- `parse_triage_output` : parsing + validation + mapping ;
- `MockStructuredModel` : faux modèle déterministe ;
- `triage_ticket` : point d’entrée agentique ;
- `build_user_reply` : extension facultative.

## Cas valide

Un ticket de double facturation doit être routé vers `billing_ops`.

Exemple :

```python
decision = triage_ticket("Je suis très énervé, vous m’avez facturé deux fois.")
assert decision.category == "billing"
assert decision.owner_team == "billing_ops"
assert decision.action_required is True
```

## Cas enum invalide

Une sortie comme :

```json
{
  "category": "finance"
}
```

doit être rejetée, car `finance` n’est pas dans l’enum autorisée.

La solution ne doit pas convertir silencieusement `finance` en `billing`.

## Cas champ manquant

Une sortie sans `confidence` doit être rejetée.

La solution ne doit pas attribuer automatiquement `0.5`, car cela masquerait l’erreur du modèle.

## Points d’attention

Un bon challenge n’est pas seulement un code qui fonctionne sur le cas nominal.

Il doit aussi montrer que l’apprenant comprend les frontières de sécurité :

- le modèle peut se tromper ;
- le JSON peut être invalide ;
- une valeur peut être plausible mais hors contrat ;
- une décision critique doit rester contrôlée par l’application.
