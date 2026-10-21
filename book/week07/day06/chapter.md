# Semaine 7 — Jour 6 : Human in the loop et décisions traçables


## 1. La validation humaine est un protocole
Une pause dans un workflow ne suffit pas à définir une autorisation. Il faut savoir qui décide, sur quoi, pendant combien de temps et avec quelles conséquences. Le fil rouge exige une proposition stockée, une empreinte de son contenu, une identité de relecture et une date d’expiration. Tous les brouillons sont relus : aucune confiance déclarée par le générateur ne contourne cette étape.

n8n propose plusieurs mécanismes d’attente et de revue humaine. Nous utilisons ici un workflow distinct de réception de décision et un état durable côté backend. Cela évite de conserver une requête HTTP ouverte pendant une heure et laisse la décision arriver dans une nouvelle exécution. Le nœud Wait et la revue d’outils d’agent sont étudiés comme variantes; ils ne sont pas présents dans les exports livrés.

## 2. Ce qui est approuvé doit être stable
Le moteur calcule un SHA-256 du JSON canonique de la proposition. Le relecteur renvoie ce hash avec approve ou reject. Le moteur compare au hash courant. Si le texte a changé, une ancienne décision échoue. Le hash n’est ni une signature du relecteur ni un secret : il lie simplement la décision au contenu attendu.

La date d’expiration est appliquée au moment de décider. Il n’est pas nécessaire d’attendre le passage du scheduler pour refuser une validation tardive. Le scheduler peut ensuite rendre l’état expired visible. Une approbation avant expiration qui est déjà publiée reste une publication valide; une répétition identique renvoie son résultat sans créer une deuxième ligne.

## 3. Identité et rôle dans le lab
Deux tokens distincts séparent les opérations de service des opérations de décision. Le serveur associe le token de revue au seul acteur reviewer-demo. Un champ reviewer envoyé par le client n’est pas accepté comme preuve d’identité. Le workflow n8n de décision utilise un credential de réception protégé et un credential backend réservé à la revue.

Cette identité à token partagé sert à un lab local. Elle n’identifie pas plusieurs personnes et ne fournit pas une gouvernance d’entreprise. Pour un environnement partagé, remplacer ce mécanisme par OIDC, mapping des sujets aux rôles, contrôle par ressource et audit de l’acteur. Une URL de reprise difficile à deviner ne suffit pas à authentifier une personne.

## 4. Refus et répétitions
Reject termine le job sans publication. Répéter reject avec le même acteur et la même proposition est admis. Tenter approve ensuite retourne un conflit; le moteur ne change pas une décision terminale silencieusement. Une correction du brouillon ou une nouvelle validation exige un parcours explicite supplémentaire, hors périmètre du lab.

Le refus ne doit pas être traité comme une erreur transitoire. Il faut afficher la décision au demandeur et permettre une suite métier adaptée. Dans ce projet, le statut suffit; aucun message externe ni aucune notification réelle n’est envoyé.

## 5. Réduction des risques et audit
La publication simulée et la transition published sont commitées ensemble. L’audit contient accepted, draft_created et published ou rejected. Il ne recopie pas le contenu du ticket. Cette table démontre la traçabilité logique; elle n’est pas un journal inviolable puisque le propriétaire de la base peut la modifier.

Le relecteur doit voir le ticket, le brouillon et la conséquence de la décision. Un bouton « oui » sans contexte augmente les validations mécaniques. Les exports n8n ne fournissent pas de portail de revue; le lab utilise GET /jobs et un POST explicite. L’ergonomie d’un portail est une proposition d’amélioration, pas un composant caché.

## À retenir
Une revue sûre lie une identité autorisée, un contenu stable, une fenêtre temporelle et une transition précise. Le clic n’est que l’interface de ce protocole.
