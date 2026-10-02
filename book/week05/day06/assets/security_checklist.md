# Checklist de sécurité et de qualité

## Lab

- [ ] Installation en environnement virtuel depuis requirements.txt.
- [ ] Configuration générée localement, jamais ajoutée au dépôt.
- [ ] Clé absente/invalide refusée.
- [ ] Scope manquant refusé.
- [ ] Isolation documentaire par route directe, chat et outil.
- [ ] Outil inconnu et arguments supplémentaires refusés.
- [ ] Quota partagé, concurrent et réinitialisé à la bonne échéance.
- [ ] Prompt et secrets absents des logs et erreurs.
- [ ] Corrigé du challenge exécuté et testé.
- [ ] Notebook étudiant sans corrections, enseignant complet.

## Avant un déploiement réel

- [ ] TLS et limitation du corps HTTP en octets, même sans Content-Length.
- [ ] Identité adaptée aux clients, validation JWT complète si utilisé.
- [ ] Secrets techniques séparés et révocation définie.
- [ ] Limitation avant authentification et quotas distribués atomiques.
- [ ] Délais, sortie maximale, retries et itérations bornés.
- [ ] Isolation SQL, ACL et cache testées sous plusieurs tenants.
- [ ] Autorisation de chaque outil et politique d'egress.
- [ ] Audit protégé, rétention et masquage proxy/APM.
- [ ] Évaluation d'injections avec un vrai fournisseur.

Cette seconde liste est un plan d'intégration, pas une assertion de conformité du lab.
