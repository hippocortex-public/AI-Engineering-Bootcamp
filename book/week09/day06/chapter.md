# S9 J6 — Mémoire d’agents : isolation, durée et invalidation


## 1. Ce jour prolonge les fondamentaux de mémoire
S2 présentait les types de mémoire et S3 le partage d’état. Ici l’objectif est opérationnel : que devient une information mémorisée quand la source change, quand la session se termine ou quand un autre utilisateur interroge le système ? La recherche documentaire et la mémoire d’agent ne doivent pas se transformer en un même sac de textes sans politique de cycle de vie.

Le store possède une table memory distincte. Une note peut représenter une préférence de forme ou une synthèse dérivée d’un document. Les notes ne sont jamais utilisées comme preuves factuelles dans la réponse extractive. Les citations finales proviennent exclusivement des chunks courants et autorisés.

## 2. Définir la clé de portée
Une note est identifiée par tenant, user_id, session_id et note_id. Connaître le même note_id dans une autre session ne donne pas accès au contenu. Le code reçoit ces champs d’un contexte supposé fiable; il ne fournit pas d’authentification. Un raccord réel dériverait tenant et utilisateur d’une identité vérifiée.

Le lab ne crée pas de mémoire globale ni de profil personnel implicite. Une note de style pour Alice dans s1 n’apparaît ni chez Bob dans s1, ni chez Alice dans s2. Étendre une préférence à toutes les sessions serait une décision de produit et de consentement à définir séparément.

## 3. TTL et horloge
remember enregistre expires_at = now + ttl. recall ne retourne que les notes dont expires_at est strictement supérieur à now. Une note expire donc exactement à l’échéance. Les tests injectent l’horloge pour éviter une attente réelle et rendre les frontières reproductibles.

L’expiration est logique : une ligne expirée peut encore se trouver dans le fichier SQLite. Le module n’exécute pas de purge automatique. forget supprime une note du store courant; sauvegardes et autres copies nécessiteraient une politique distincte. Ne pas confondre invisibilité à la lecture et effacement de toutes les copies physiques.

## 4. Mémoire liée à une source
Une note peut référencer doc_id. Le store conserve alors la version courante au moment de l’écriture. Lors de recall, une jointure vérifie que la source possède encore cette version. Une mise à jour masque donc une ancienne synthèse au lieu de la présenter comme un savoir récent.

La suppression documentaire retire aussi les notes référencées dans le tenant. Réingérer plus tard un document de même nom ne ressuscite pas ces notes supprimées. Une note sans source reste une note de session; elle ne reçoit pas artificiellement un statut de vérité documentaire.

## 5. Empoisonnement et corrections
Un texte reçu peut demander de mémoriser une fausse préférence, une autorisation ou un secret. La présence dans un échange ne suffit pas à autoriser l’écriture en mémoire. L’application doit distinguer contenu à utiliser une fois et fait durable à conserver. Le lab expose une API explicite, sans extraction automatique de « faits » par un modèle.

Une correction peut remplacer la note de même clé; un oubli la supprime. Il n’y a pas d’historique des anciennes notes ni de journal d’approbation dans cette table. Ces extensions peuvent être utiles, mais ne sont pas présentées comme déjà disponibles. Une note qui prétend modifier les droits ne change aucun filtre de recherche.

## 6. Expérience du jour
Créer une préférence, tester les trois axes d’isolation, puis avancer l’horloge jusqu’à la date exacte d’expiration. Créer ensuite une note liée à une source et modifier cette source. Vérifier qu’aucune réponse documentaire ne cite la note comme autorité. Cette séparation évite de transformer une mémoire commode en vecteur de fuite ou de connaissance périmée.

## À retenir
Une mémoire exploitable a une portée, une durée, une provenance et une règle d’invalidation. Sa récupération ne lui confère pas automatiquement une valeur de preuve.
