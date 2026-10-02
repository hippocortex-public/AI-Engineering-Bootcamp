# Exercices — Déploiement

## Exercice 1 — Healthy, ready ou correct ? (principal)

L'API retourne 200 sur `/health/live`, PostgreSQL répond à `pg_isready`, mais la
readiness retourne 503. Proposer deux causes compatibles avec ces observations et
la vérification utile pour chacune. Pourquoi la liveness ne consulte-t-elle pas la DB ?

## Exercice 2 — Données et mots de passe (principal)

Après un premier démarrage, vous modifiez le fichier du mot de passe applicatif et
le script SQL d'initialisation, puis relancez Compose. L'API ne se connecte plus.
Expliquer pourquoi. Décrire une rotation et une migration correctes sans supprimer
le volume pour « réparer ».

## Exercice 3 — Choisir un rollback (principal)

Release-002 utilise une nouvelle colonne obligatoire et la migration a supprimé
une ancienne colonne requise par release-001. Les smoke tests échouent.
Peut-on simplement restaurer l'image 001 ? Proposer une séquence expand/contract.

## Exercice 4 — Partage du quota (approfondissement)

Instancier deux backends pointant vers la même instance fakeredis, puis faire consommer
le quota du même principal. Vérifier que changer de backend ne crée pas un nouveau
budget. Expliquer la différence entre ce test et deux Redis indépendants.

## Exercice 5 — Contrôle de livraison (approfondissement)

Compléter une checklist avant/après livraison : référence d'image, configuration,
schéma, sauvegarde, readiness, tests fonctionnels, isolation, métriques et rollback.
Pour chaque élément, préciser une preuve concrète plutôt qu'un simple « OK ».
