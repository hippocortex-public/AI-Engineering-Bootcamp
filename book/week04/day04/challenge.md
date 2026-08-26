# Challenge — Construire une Memory Layer intégrable

## Contexte

Tu construis le mini-framework d'agents du bootcamp. Les jours précédents ont introduit :

- une architecture de framework ;
- une abstraction `Agent` ;
- un `Tool Registry`.

Tu dois maintenant intégrer une couche mémoire.

## Objectif

Créer une Memory Layer qui permet à un agent de :

1. stocker des préférences utilisateur ;
2. stocker des faits vérifiés ;
3. retrouver les mémoires pertinentes ;
4. respecter la visibilité ;
5. oublier un utilisateur ;
6. produire un snapshot JSON.

## Contraintes

- Python standard library uniquement.
- Pas de dépendance externe.
- Pas de base vectorielle.
- Pas de stockage global partagé sans namespace.
- Les tests doivent être déterministes.

## Critères d'acceptation

Le challenge est réussi si :

- `MemoryStore.add` valide les champs obligatoires ;
- `MemoryStore.retrieve` filtre par namespace ;
- `private`, `shared`, `public` sont respectés ;
- les records expirés sont exclus par défaut ;
- `forget_namespace` supprime uniquement le namespace demandé ;
- un snapshot peut être exporté puis restauré ;
- les écritures sont auditées ;
- les PII simples sont redacted.

## Extension optionnelle

Ajoute une stratégie `promote_event` qui transforme certains événements en mémoire durable uniquement s'ils sont réutilisables.
