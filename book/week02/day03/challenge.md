# Challenge — Agent de triage support avec sortie structurée

## Contexte

Tu construis un assistant IA mono-agent pour une équipe support.

L’agent reçoit un ticket utilisateur et doit produire une décision structurée, validable et exploitable par un backend.

## Objectif

Implémenter ou compléter un pipeline qui transforme un ticket en `TriageDecision`.

Le pipeline doit :

1. produire une sortie JSON ;
2. parser cette sortie ;
3. valider le contrat ;
4. convertir la sortie validée en objet Python ;
5. refuser explicitement les sorties invalides.

## Schéma attendu

La sortie doit respecter le contrat suivant :

```json
{
  "category": "billing | technical | account | shipping | other",
  "priority": "low | medium | high | critical",
  "sentiment": "neutral | frustrated | angry | satisfied",
  "summary": "string",
  "action_required": "boolean",
  "next_action": {
    "owner_team": "support_l1 | billing_ops | technical_ops | account_ops",
    "rationale": "string"
  },
  "confidence": "number between 0 and 1"
}
```

Tous les champs sont obligatoires.

Aucune propriété supplémentaire n’est autorisée.

## Contraintes

- Ne pas utiliser de dépendance externe.
- Ne pas faire confiance au JSON sans validation.
- Ne pas corriger silencieusement les valeurs invalides.
- Écrire au moins trois tests :
  - un cas valide ;
  - un cas avec enum invalide ;
  - un cas avec champ manquant.
- Le code doit rester lisible pour un AI Backend Engineer junior.

## Scénarios à couvrir

### Scénario 1 — Double facturation

```text
Je suis très énervé, vous m’avez facturé deux fois ce mois-ci.
```

Attendu :

- catégorie : `billing` ;
- priorité : `high` ou `critical` ;
- sentiment : `angry` ou `frustrated` ;
- équipe : `billing_ops`.

### Scénario 2 — Problème de connexion

```text
Depuis ce matin je ne peux plus me connecter à mon compte.
```

Attendu :

- catégorie : `technical` ou `account` ;
- priorité : au moins `medium` ;
- équipe : `technical_ops` ou `account_ops`.

### Scénario 3 — Question simple

```text
Bonjour, je voudrais savoir où trouver mes anciennes factures.
```

Attendu :

- catégorie : `billing` ;
- priorité : `low` ou `medium` ;
- action requise : `true` ;
- équipe : `billing_ops` ou `support_l1`.

## Extension facultative

Ajoute une fonction `build_user_reply(decision)` qui génère une réponse utilisateur à partir de la décision validée.

La réponse utilisateur ne doit pas être mélangée avec le JSON machine.
