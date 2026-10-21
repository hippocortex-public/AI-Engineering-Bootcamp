# Semaine 7 — Jour 4 : Fiabilité, reprises et erreurs


## 1. Toutes les erreurs ne se rejouent pas
Un timeout ou une indisponibilité temporaire peut disparaître. Un contrat invalide ne se corrige pas avec une attente. Le moteur traite TemporaryFailure comme une erreur temporaire et InvalidEvent comme un défaut permanent. Un adaptateur fournisseur doit convertir les erreurs pertinentes dans ces types; il ne doit pas transformer toutes les exceptions en « retry ».

Les erreurs de programmation inattendues remontent à l’appelant. Les cacher dans une boucle de reprise rendrait le diagnostic difficile et pourrait répéter des actions incorrectes. Sur n8n, une erreur de transport vers le backend relève du workflow technique; sur le backend, une erreur du générateur relève du job métier. Ces deux niveaux doivent être observés séparément.

## 2. Reprise bornée et dates persistées
Le moteur augmente attempts puis inscrit ready_at. Après les échecs successifs, les délais sont de 2 puis 4 secondes; le troisième échec termine en dead_letter. Trois tentatives signifient un appel initial et deux reprises, pas trois reprises supplémentaires. Le scheduler ne doit pas traiter un job avant ready_at.

Le lab n’effectue aucun sleep dans le traitement. Il libère la main et laisse le prochain tick trouver le job éligible. Les tests utilisent une horloge injectable : augmenter une valeur reproduit un délai sans ralentir la suite. En production, ajouter du jitter et respecter les consignes du fournisseur, notamment Retry-After si disponible. Sans jitter, une panne commune peut provoquer une reprise simultanée de tous les clients.

## 3. Les reprises imbriquées multiplient les appels
Si un SDK retente trois fois et que le workflow retente trois fois l’appel entier, le fournisseur peut recevoir jusqu’à neuf appels. Il faut définir le propriétaire du budget de reprise et une durée totale. Dans ce lab, le moteur possède le budget métier. Un échec du POST /tick peut laisser des jobs déjà traités : le tick suivant vérifie leur état au lieu de générer systématiquement à nouveau.

Le traitement est limité à cent jobs éligibles par tick. C’est une borne de batch, pas un mécanisme complet de backpressure. Il n’y a ni quotas par client, ni ordonnancement équitable, ni workers parallèles. Si le débit d’entrée dépasse celui du traitement, la file durable grossit. Le compteur des états permet de voir l’accumulation, mais une exploitation réelle ajouterait l’âge du plus ancien job.

## 4. Quarantaine et replay
Dead_letter signifie que le traitement automatique est arrêté. Un opérateur examine le contrat, les tentatives et le type d’erreur. Après correction de la cause, il demande un replay explicite. Le replay remet le job à received et remet le compteur à zéro; cette action apparaît dans l’audit. Le endpoint est protégé par le token de relecture du lab.

La séparation entre une dead letter et un refus humain est importante. Le refus est un résultat métier accepté; il ne doit pas devenir un incident à retenter. Une validation expirée ne se relance pas automatiquement avec une ancienne autorisation.

## 5. Outbox et effets externes
Le lab écrit la publication simulée dans la même base que le job. Avec un destinataire externe, la transaction locale ne pourrait pas inclure son acceptation réseau. Une outbox enregistre une intention de publication avec la transition métier, puis un dispatcher tente l’envoi. Cette intention durable supprime la perte entre décision locale et lancement de l’envoi, mais le dispatcher peut toujours répéter un envoi. Le destinataire doit dédupliquer ou le système doit réconcilier.

L’outbox n’est pas implémentée dans ce moteur pédagogique; elle est étudiée comme une extension. Le cours distingue volontairement l’invariant démontré localement de la garantie attendue pour un service tiers.

## À retenir
Une reprise fiable possède une catégorie d’erreur, un budget, une date d’éligibilité et une sortie observable. Un replay est une opération contrôlée, pas une boucle infinie.
