# Semaine 7 — Jour 3 : Événements, contrats et idempotence


## 1. Un événement représente un fait
`support.requested` indique qu’une demande a été reçue par le système amont. Le fait garde le même identifiant lors d’une nouvelle livraison. Une commande comme « préparer un brouillon » exprime une intention et peut être refusée. Une réponse HTTP indique le résultat d’un échange technique, sans devenir automatiquement un événement métier.

Notre enveloppe minimale possède `event_id`, `schema_version`, `type`, `ticket_id` et `text`. Elle n’implémente pas CloudEvents; ce standard serait une option d’interopérabilité. `ticket_id` corrèle plusieurs faits pour une même demande, tandis que `event_id` distingue les faits. Ajouter une correction à un ticket exige un nouvel événement, pas une nouvelle livraison du précédent.

## 2. Le contrat est une frontière
Le validateur exige des champs connus, une version entière égale à 1 et un type reconnu. Les valeurs textuelles sont non vides et bornées. Même une valeur JSON `true` est refusée pour la version : Python considère normalement bool comme une sous-classe de int, ce qui peut rendre un contrôle naïf trop permissif.

Un contrat strict révèle tôt une incompatibilité. Il exige aussi une politique de migration. Si un producteur ajoute un champ, ce consommateur version 1 le refusera. L’exercice vise à rendre le comportement explicite, pas à prescrire le rejet de tous les champs supplémentaires dans toutes les architectures. Une évolution compatible peut choisir d’ignorer certains champs, à condition de le documenter et de le tester.

## 3. Au moins une fois signifie doublons possibles
Le producteur peut perdre la réponse après que le backend a commité. Il ne sait pas si son événement a été accepté et le renvoie. Le réseau ne fournit pas une garantie métier « exactement une fois ». Le backend compare l’identifiant et le contenu canonique, puis retourne le job existant pour un doublon identique.

La clé primaire `event_id` protège le stockage. Le contenu sérialisé avec des clés triées neutralise l’ordre des clés JSON. Si le même identifiant est envoyé avec un autre texte, le service répond 409. Supprimer simplement le doublon sans comparer son contenu masquerait un bug du producteur ou une collision d’identifiants.

## 4. Déduplication et idempotence ne se confondent pas
La déduplication reconnaît une livraison déjà reçue. L’idempotence garantit qu’une répétition admissible n’ajoute pas un nouvel effet. La publication locale utilise une clé primaire sur event_id et une transition transactionnelle. Deux demandes distinctes avec deux identifiants peuvent toujours publier deux réponses pour le même ticket : c’est un problème métier différent. Une politique par ticket doit être définie si ce comportement est indésirable.

Ne promettez pas un « exactly once » universel à partir de cette table. Un fournisseur de messagerie externe peut accepter l’envoi puis perdre la connexion avant l’accusé de réception. Il faut un identifiant d’effet stable, une idempotency key supportée par le fournisseur, ou une réconciliation. Sans ce support, une livraison répétée peut produire un doublon externe.

## 5. Accusé de réception et durée de rétention
On répond après la persistance du fait. Dans le lab, les jobs et les identifiants restent conservés; il n’y a pas de purge des jobs métier. Une installation réelle doit définir combien de temps un identifiant reste dédupliquable. Purger trop tôt permet à une livraison tardive de redevenir un événement neuf.

## À retenir
Un event_id stable rend une nouvelle livraison reconnaissable. Il ne résout ni l’ordre des événements d’un ticket, ni l’atomicité avec un système externe, ni toutes les règles métier de duplication.
