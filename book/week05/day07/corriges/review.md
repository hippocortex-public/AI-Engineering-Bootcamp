# Revue pédagogique — Déploiement

## Ce qui doit être maîtrisé

Séparation code/configuration/données ; santé applicative et des dépendances ;
identité non root et autorisation API ; quota partagé ; cache avec contrôle d'accès ;
référence de release et compatibilité de schéma.

## Pièges à repérer

Assimiler une image à une sauvegarde ; croire que l'init SQL rejoue les migrations ;
modifier un fichier de secret sans modifier le service cible ; oublier les clients
sur un ancien secret ; effacer des volumes lors du rollback ; conclure à la réussite
avec une seule liveness ; annoncer du zéro downtime avec le remplacement Compose.

## Barème proposé

| Critère | Points |
|---|---|
| Image et secrets correctement expliqués | 4 |
| Stack, volumes et santé compris | 5 |
| Sécurité, cache et quotas vérifiés | 4 |
| Livraison/rollback justifiés | 5 |
| Limites de validation reconnues | 2 |

Réussite proposée : 14/20 sans suppression involontaire de données ni fuite inter-tenant.
La validation pédagogique appartient à l'apprenant ; les fichiers de suivi ne
confondent pas production de contenu et achèvement de la formation.

## Propositions d'amélioration

Sans changer les spécifications : verrouiller les images par digest, ajouter une
collecte métrique, pratiquer une restauration PostgreSQL et intégrer un vrai
fournisseur à une campagne de tests adversariaux. Le provisioning cloud et une
bascule blue/green peuvent prolonger le lab sans modifier la roadmap.
