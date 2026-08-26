# Exercices — Structured Outputs

## Exercice 1 — Identifier la bonne stratégie

Pour chaque besoin, indique le mécanisme le plus adapté :

- texte libre ;
- JSON mode ;
- function calling ;
- Structured Outputs.

### Cas A

L’utilisateur demande une explication pédagogique sur le fonctionnement d’un transformeur.

### Cas B

L’application doit appeler une fonction `get_invoice(invoice_id)`.

### Cas C

Le backend doit recevoir une décision de routage contenant `category`, `priority` et `owner_team`.

### Cas D

Un prototype doit simplement produire un JSON valide pour une démonstration interne non critique.

## Exercice 2 — Concevoir un schéma

Conçois un schéma JSON pour classifier une demande utilisateur avec les champs suivants :

- `intent` : parmi `order_status`, `refund`, `technical_issue`, `other` ;
- `requires_tool` : booléen ;
- `missing_fields` : liste de chaînes ;
- `confidence` : nombre entre 0 et 1.

Contraintes :

- tous les champs sont obligatoires ;
- aucune propriété supplémentaire n’est acceptée ;
- les valeurs de `intent` sont strictement limitées.

## Exercice 3 — Détecter les erreurs

Le schéma attendu impose :

```json
{
  "category": "billing | technical | account | shipping | other",
  "priority": "low | medium | high | critical",
  "confidence": "number between 0 and 1"
}
```

La sortie suivante est produite :

```json
{
  "category": "finance",
  "priority": "urgent",
  "confidence": "0.9",
  "explanation": "Client très mécontent"
}
```

Liste toutes les erreurs de contrat.

## Exercice 4 — Mapper vers un objet métier

À partir de la sortie suivante :

```json
{
  "category": "technical",
  "priority": "high",
  "sentiment": "frustrated",
  "summary": "Le client ne peut plus se connecter.",
  "action_required": true,
  "next_action": {
    "owner_team": "technical_ops",
    "rationale": "Le problème concerne l'accès au compte."
  },
  "confidence": 0.88
}
```

Décris l’objet métier Python que tu créerais.

Tu n’as pas besoin d’écrire tout le code, mais tu dois préciser :

- le nom de la classe ;
- les champs ;
- les types attendus ;
- ce qui doit avoir été validé avant instanciation.

## Exercice 5 — Stratégie de récupération

Une sortie structurée échoue parce que le modèle a oublié le champ `confidence`.

Propose une stratégie de récupération robuste.

Ta réponse doit inclure :

- ce que le système journalise ;
- ce qu’il redemande au modèle ;
- le fallback si la deuxième tentative échoue ;
- pourquoi il ne faut pas inventer une confiance par défaut sans le signaler.
