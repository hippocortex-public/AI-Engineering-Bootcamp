# Exercices

## Exercice 1 — Identifier les responsabilités de la couche API

Classe les responsabilités suivantes en deux catégories : `API HTTP` ou `service applicatif`.

1. Lire l'en-tête `X-API-Key`.
2. Classer l'intention utilisateur.
3. Retourner un code `401`.
4. Stocker un tour dans une session.
5. Valider la taille du message.
6. Générer la réponse métier.
7. Renvoyer un `X-Request-ID`.
8. Masquer les emails avant stockage.

## Exercice 2 — Étendre le contrat `ChatRequest`

Ajoute mentalement un champ `channel` autorisé parmi :

- `web`
- `mobile`
- `slack`
- `api`

Explique :

1. où le champ doit être validé ;
2. pourquoi il ne doit pas être laissé comme chaîne libre ;
3. comment il peut aider l'observabilité.

## Exercice 3 — Concevoir une erreur stable

Propose une enveloppe JSON pour une erreur `429 Too Many Requests`.

Elle doit contenir au minimum :

- code d'erreur ;
- message lisible ;
- request ID ;
- limite ;
- nombre restant.

## Exercice 4 — Tester sans serveur réseau

Explique pourquoi `TestClient` est adapté pour tester une API FastAPI pendant le développement.

Donne deux cas qui doivent être testés en HTTP et non uniquement au niveau fonction Python.

## Exercice 5 — API publique cumulative

Explique pourquoi le fichier `ai_platform/__init__.py` du jour 2 doit conserver les exports du jour 1.

Que risque-t-on si chaque jour réécrit ce fichier de façon isolée ?
