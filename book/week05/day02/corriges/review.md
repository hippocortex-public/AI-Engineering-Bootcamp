# Review formateur

## Ce que l'apprenant doit avoir compris

- FastAPI est une frontière de production, pas une simple démo HTTP.
- Les schémas Pydantic protègent le système avant l'appel modèle.
- Les dépendances FastAPI permettent de centraliser auth et contrôles.
- Le request ID est indispensable au diagnostic production.
- Les erreurs doivent être stables pour les clients.
- Un rate limiter mémoire est pédagogique, pas distribué.
- `ai_platform/__init__.py` doit rester cumulatif.

## Points d'attention

- Ne pas mélanger logique agentique et fonction de route.
- Ne pas stocker de PII brute.
- Ne pas retourner les exceptions Python telles quelles.
- Ne pas introduire de dépendance externe non maîtrisée dans les tests.
- Ne pas casser les exports du jour 1.

## Questions de validation orale

1. Où placerais-tu un appel à Redis pour le rate limiting ?
2. Où placerais-tu l'appel au modèle OpenAI ?
3. Pourquoi `ChatResponse` doit-il être stable ?
4. Quelle donnée mettrais-tu dans les logs et quelle donnée éviterais-tu ?
5. Comment versionnerais-tu `/v1/chat` si le contrat change ?

## Propositions d'amélioration

Ces propositions ne modifient pas les spécifications figées :

- ajouter une gateway locale dans une future journée production ;
- ajouter un module `ai_platform/security.py` au jour sécurité ;
- ajouter une stratégie de versioning d'API plus avancée ;
- brancher l'observabilité de la semaine 4 sur les middlewares API.
