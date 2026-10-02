# Checklist de livraison

## Avant

- [ ] Commit et image identifiés ; dépendances et base testées.
- [ ] Build excluant secrets, tests et environnements locaux.
- [ ] Secrets configurés sans re-génération incohérente.
- [ ] Rôle SQL applicatif limité ; réseau backend sans publication de ports.
- [ ] Schéma et image précédente compatibles ; backup/restauration planifiés.
- [ ] Tests auth, cache, quotas et refus inter-tenant réussis.
- [ ] Probes, délais et ressources cohérents avec la charge.

## Après

- [ ] Conteneurs healthy ; readiness et smoke tests réussis.
- [ ] Refus légitimes et utilisateurs autorisés vérifiés.
- [ ] Erreurs, latence et cache observés.
- [ ] Référence de version active enregistrée ; rollback réalisable.
- [ ] Volumes et secrets conservés.

## Avant exposition publique

- [ ] TLS, reverse proxy, taille des corps et limitation avant authentification.
- [ ] Identités et rotation adaptées au service réel.
- [ ] Egress, sauvegarde, collecte et procédure d'incident validés.
- [ ] Garanties de quota et budget financier définies.

La checklist documente les contrôles à réaliser ; elle ne certifie pas un déploiement
que cet environnement de génération ne peut pas démarrer.
