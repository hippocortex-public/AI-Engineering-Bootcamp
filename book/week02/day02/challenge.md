# Challenge — Assistant de support avec Function Calling

## Contexte

Vous devez construire le cœur d’un assistant IA mono-agent pour un service client e-commerce.

L’assistant doit pouvoir :

1. récupérer le statut d’une commande ;
2. estimer un remboursement ;
3. créer un ticket de support ;
4. refuser proprement les appels invalides.

Le challenge se concentre sur l’architecture de function calling, pas sur l’appel à une API LLM réelle.

## Contraintes

Le projet doit être exécutable localement avec Python standard.

Vous devez éviter :

- `eval`;
- `exec`;
- `globals()` pour appeler une fonction ;
- l’exécution d’un outil non déclaré ;
- l’acceptation d’arguments non prévus.

## API métier attendue

Vous pouvez utiliser ces fonctions métier :

```python
def get_order_status(order_id: str) -> dict:
    ...

def estimate_refund(order_id: str, reason: str) -> dict:
    ...

def create_support_ticket(order_id: str, issue: str, priority: str) -> dict:
    ...
```

## Travail demandé

### Partie 1 — Contrats d’outils

Déclarez trois schémas :

- `get_order_status`;
- `estimate_refund`;
- `create_support_ticket`.

Chaque schéma doit contenir :

- `name`;
- `description`;
- `parameters.type`;
- `parameters.properties`;
- `parameters.required`;
- `parameters.additionalProperties`.

### Partie 2 — Registre d’outils

Implémentez une classe `ToolRegistry`.

Elle doit permettre :

- d’enregistrer un schéma et une fonction ;
- de lister les schémas exposés au modèle ;
- de valider un appel ;
- de dispatcher un appel.

### Partie 3 — Boucle agentique

Implémentez une classe `SupportAgent`.

Elle doit :

1. recevoir un message utilisateur ;
2. obtenir un appel d’outil depuis un planificateur simulé ;
3. exécuter l’appel via le registre ;
4. retourner une réponse finale ;
5. retourner une erreur contrôlée si l’appel est invalide.

### Partie 4 — Tests

Ajoutez au moins quatre tests :

1. appel valide de `get_order_status`;
2. refus d’un outil inconnu ;
3. refus d’un argument supplémentaire ;
4. refus d’une valeur `priority` hors enum.

### Partie 5 — Analyse

Rédigez une note courte expliquant :

- quelles décisions restent côté application ;
- quelles décisions sont laissées au modèle ;
- quelles protections empêchent une exécution dangereuse.

## Critères d’évaluation

| Critère | Attendu |
|---|---|
| Contrat d’outil | Schémas clairs, spécifiques et stricts |
| Validation | Arguments manquants, types, enum et extras gérés |
| Dispatch | Aucun appel dynamique non contrôlé |
| Agent | Boucle lisible et testable |
| Erreurs | Résultats structurés |
| Tests | Cas nominal et cas d’échec couverts |
| Style | Code simple, professionnel, exécutable |

## Bonus

Ajoutez une trace d’observabilité pour chaque appel :

```json
{
  "tool": "get_order_status",
  "ok": true,
  "duration_ms": 3
}
```

Le bonus ne doit pas complexifier inutilement le design.
