# Corrigé — Exercices — Jour 6

## Exercice 1 — Identifier les couches de contexte

| Élément | Catégorie |
|---|---|
| `Tu es un agent support interne.` | instruction système |
| `ticket_id = T-204` | état de tâche |
| `L’utilisateur préfère les réponses courtes.` | mémoire longue |
| Dernier message utilisateur | historique récent |
| `billing_policy.md` | ressource |
| `get_invoice_status` | outil |
| Tentative précédente d’outil | trace |

## Exercice 2 — Construire un context pack

À injecter :

- A — instruction système support ;
- C — état courant ;
- D — mémoire de préférence, si elle est autorisée et utile au format de réponse ;
- E — ressource de politique de relance ;
- F — outil de statut facture.

À exclure :

- B — ancien ticket RH, hors sujet ;
- G — `delete_invoice`, action dangereuse et inutile ;
- H — trace ancienne non liée.

## Exercice 3 — Budget

Budget : 100 tokens.

Sélection :

| Élément | Tokens |
|---|---:|
| system | 20 |
| task_state | 30 |

Total : 50.

`billing_policy` ferait passer le total à 120. Il doit être compressé, résumé ou récupéré partiellement.

`user_preference` peut être ajoutée si elle est utile, total 65.

`old_trace` est exclue car priorité faible.

## Exercice 4 — Visibilité

Un élément `private` peut contenir :

- raisonnement interne ;
- informations sensibles ;
- données destinées à un agent spécialisé ;
- diagnostics non validés ;
- secrets opérationnels.

Il ne doit pas être injecté sans transformation explicite, car cela peut créer une fuite d’information et influencer un agent qui n’a pas besoin de cette donnée.

## Exercice 5 — Déduplication

Les deux phrases portent la même information. Une déduplication normalisée supprime :

- espaces inutiles ;
- différences de casse ;
- variations mineures de format.

Elles doivent donc être considérées comme doublons.

## Exercice 6 — PII

Résultat attendu :

```text
Contacte Alice à [REDACTED_EMAIL] ou au [REDACTED_PHONE].
```

## Exercice 7 — MCP

Un serveur MCP peut exposer beaucoup de ressources. Les injecter toutes crée :

- bruit ;
- coût ;
- risque de fuite ;
- conflit de sources ;
- confusion d’outil ;
- latence.

Le client doit découvrir les ressources, puis sélectionner seulement celles qui répondent à l’objectif courant.

## Exercice 8 — Tests indispensables

Exemples de tests :

1. le moteur respecte le budget ;
2. les éléments `private` sont exclus si non autorisés ;
3. les emails et téléphones sont réduits ;
4. les doublons normalisés sont supprimés ;
5. les éléments critiques sont prioritaires ;
6. les raisons de rejet sont tracées.
