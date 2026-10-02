# Questions d'entretien — Déploiement IA

1. Que doit contenir l'image d'un service IA et que faut-il fournir au démarrage ?
2. Pourquoi `depends_on` ne remplace-t-il pas une stratégie de reprise réseau ?
3. Quelle différence entre liveness et readiness ?
4. Pourquoi un UID 10001 n'est-il pas un utilisateur IAM ou une identité client ?
5. Une réponse en cache peut-elle contourner une révocation documentaire ?
6. Comment rendre un quota correct lorsque plusieurs instances servent la même identité ?
7. Pourquoi une release avec un tag unique peut-elle encore manquer de reproductibilité ?
8. Que conserve `docker compose down` et que détruit `--volumes` ?
9. Quelles conditions permettent un rollback d'image après migration ?
10. Quels risques particuliers apportent les appels LLM longs et les retries ?

## Mise en situation

Une release passe la readiness mais produit des 403 pour tous les utilisateurs et
aucun cache hit. Proposer le diagnostic et les critères pour conserver ou annuler
la release. Ne pas journaliser les clés client pour faciliter la recherche.
