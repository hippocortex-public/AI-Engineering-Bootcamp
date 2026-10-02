# Objectifs — Déploiement IA

À la fin du jour 7, savoir :

1. Distinguer image, conteneur, configuration et données persistantes.
2. Construire une image applicative sans secrets et avec un UID non root.
3. Exécuter une stack locale avec réseaux, volumes et secrets explicites.
4. Distinguer liveness, readiness, disponibilité et validation métier.
5. Expliquer le rôle et les limites de `depends_on: service_healthy`.
6. Tester un cache et un quota partagés sans mélanger les tenants.
7. Livrer une version identifiée et vérifier son fonctionnement après démarrage.
8. Revenir à l'image précédente sans prétendre restaurer automatiquement la base.
9. Identifier les adaptations nécessaires avant un déploiement public.

## Preuves attendues

Une configuration Compose comprise, les tests Python exécutés, les neuf contrôles
de `smoke_test.py` réussis sur votre machine, et une explication du rollback avec
conservation des volumes. La validation pédagogique reste à réaliser par l'apprenant.

## Portée

Un hôte local ou une VM unique suffit au lab. La haute disponibilité, le provisioning
OpenTofu/Ansible, l'installation d'un cluster et la publication d'un service public
ne sont pas réalisés par cette livraison. Ils sont discutés comme choix d'architecture.
