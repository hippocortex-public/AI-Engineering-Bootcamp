# Exercices — Sécurité IA

## Exercice 1 — Cartographier les identités (principal)

Le frontend contient une clé du fournisseur LLM. Le backend accepte le champ
`tenant` envoyé dans le JSON. Il autorise `read_document` dès que le modèle le demande.

Identifier trois confusions. Pour chacune, proposer le composant qui doit prendre
la décision et la donnée de confiance utilisée. Temps conseillé : 4 minutes.

## Exercice 2 — Compléter une matrice d'accès (principal)

Alice possède les scopes `chat:write`, `documents:read`, `tools:read` dans alpha.
Carol possède seulement `chat:write` dans alpha. Bob appartient à beta avec tous
les scopes. Écrire le statut attendu :

1. Alice lit `alpha-guide` directement.
2. Alice lit `beta-guide` via `/chat`.
3. Carol appelle `read_document` sur `alpha-guide`.
4. Carol lance un chat sans document.
5. Bob lit `beta-guide` par outil.
6. Clé inconnue sur `/chat`.

Temps conseillé : 3 minutes. Vérifier les réponses dans le lab.

## Exercice 3 — Diagnostiquer une fuite Redis (principal)

Deux tenants envoient la même question. Le code stocke la réponse sous
`answer:<prompt_hash>`. Le document initial n'appartient qu'à alpha.

Expliquer la fuite possible, proposer une clé et décrire le contrôle nécessaire
sur un cache hit. Que change une différence de droits entre deux sujets d'alpha ?
Temps conseillé : 3 minutes.

## Exercice 4 — Ajouter une lecture privée (approfondissement)

Créer dans une copie du lab un document `alpha-finance` réservé au sujet Alice.
Étendre la politique documentaire sans déplacer le contrôle dans la seule route HTTP.
Conserver le comportement 404 pour un document non visible. Écrire les tests pour
lecture directe, chat et outil, puis pour Carol dotée de scopes de lecture.

## Exercice 5 — Démontrer un quota concurrent (approfondissement)

Remplacer temporairement la logique atomique par un contrôle puis incrément sans
verrou. Expliquer pourquoi le test concurrent peut devenir intermittent. Ne pas
conclure qu'une exécution réussie prouve l'absence de race. Restaurer le verrou.

Décrire une solution Redis atomique et la politique retenue si Redis est indisponible.

## Exercice 6 — Évaluer une injection sans fausse garantie (approfondissement)

Écrire deux charges de test : une instruction utilisateur cherchant à usurper beta,
et un document alpha cherchant à déclencher `http_fetch` sur une URL interne.
Pour chacune, préciser la règle backend, la preuve vérifiable et ce que la simulation
ne permet pas de conclure sur un véritable modèle.
