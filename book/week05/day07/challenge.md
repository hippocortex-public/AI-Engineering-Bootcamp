# Challenge — Décider une promotion ou un rollback

## Contrat

Écrire un contrôleur recevant : référence précédente, référence candidate,
`deploy(release)`, `readiness()` et `smoke()`. Les callbacks sont simulés.

- Refuser deux références identiques ou absentes.
- Refuser avant toute mutation un schéma déclaré incompatible avec le rollback.
- Déployer la candidate et vérifier readiness puis smoke tests.
- Si le déploiement ou un contrôle échoue, restaurer la précédente et revérifier.
- Si la récupération échoue, signaler explicitement une intervention nécessaire.
- Retourner la version active et si un rollback a eu lieu.

Chaque callback doit avoir un délai maximal. Le corrigé montre la décision mais
n'implémente ni le délai interne du moteur Docker ni une bascule réseau sans interruption.
L'indicateur de compatibilité vient de votre processus de livraison : le contrôleur
ne peut pas déduire la compatibilité de deux schémas à partir d'un booléen.

## Preuves attendues

Tests de succès, readiness KO, smoke KO, exception de déploiement, schéma incompatible
et rollback KO. Une note explique comment relier les callbacks aux commandes du lab
sans supprimer les volumes. Temps conseillé : 30 à 45 minutes.
