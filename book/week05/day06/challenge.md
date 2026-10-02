# Challenge — Ajouter une réservation de budget de tokens

## Scénario

Une identité peut lancer plusieurs appels simultanés. Un simple contrôle du coût
après réponse constate le dépassement quand il est déjà trop tard. Ajouter un
budget pédagogique par identité avant l'appel, sans vrai fournisseur LLM.

## Contrat attendu

- Budget de 1 000 unités de tokens estimés par couple `(tenant, subject)`.
- `reserve(principal, estimated_tokens)` retourne un identifiant opaque de réservation.
- Refuser une estimation négative, nulle ou supérieure au disponible.
- La somme consommée plus réservée ne peut pas dépasser le plafond à la réservation.
- `settle(reservation_id, actual_tokens)` consomme au plus le montant réservé et
  libère le reste ; une seconde finalisation est refusée.
- `cancel(reservation_id)` libère une réservation connue ; une seconde annulation
  est refusée.
- Les mutations doivent être atomiques entre threads.
- Les identifiants de réservation sont internes au backend, jamais acceptés tels
  quels depuis une instruction du modèle ou d'un appelant non autorisé.

Pour cet exercice, le fournisseur simulé garantit que la consommation ne dépasse
pas la réservation. Si `actual_tokens` dépasse celle-ci, rejeter la finalisation et
conserver la réservation pour rapprochement. Ne pas prétendre que cela annule une
facture réelle : ce cas doit être traité par une procédure de réconciliation.

## Livrable

Une classe testée en mémoire, un scénario de concurrence et une note de dix lignes
sur la migration Redis. Conserver ce code dans `labs/` sans modifier les contrats
partagés des jours précédents. Le corrigé contient une implémentation exécutable.

## Tests minimaux

1. Réservation, finalisation et libération correcte du reliquat.
2. Réservation trop grande refusée.
3. Isolation de deux tenants.
4. Deux finalisations ne peuvent pas compter deux fois.
5. Annulation libérant le disponible.
6. Appels concurrents ne dépassant pas le plafond.
7. Consommation réelle trop grande conservant la réservation.

Temps conseillé : 45 à 60 minutes. Il s'agit d'une unité pédagogique abstraite,
pas d'une estimation fiable des tokens d'un fournisseur.
