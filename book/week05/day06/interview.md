# Questions d'entretien — Sécurité IA

1. Pourquoi la clé du fournisseur LLM ne remplace-t-elle pas l'authentification client ?
2. Où vérifier le tenant dans une chaîne API → RAG → outil → PostgreSQL ?
3. Un prompt système interdit d'accéder aux données d'autres clients. Est-ce suffisant ?
4. Pourquoi un appel d'outil proposé par le modèle doit-il être autorisé à nouveau ?
5. Quels risques un cache de réponses peut-il introduire ?
6. Quelles différences entre un quota de requêtes et un budget de tokens ?
7. Comment empêcher le contournement du quota par une rotation de clé ?
8. Quelles données de sécurité journaliser et lesquelles éviter ?
9. Pourquoi décoder un JWT n'est-il pas le valider ?
10. Que changer avant de lancer ce lab avec quatre workers derrière un proxy ?

## Mise en situation

Une API répond 200 et ses temps de réponse sont stables. Un client signale avoir
reçu un extrait qui appartient à une autre organisation. Proposer les premières
mesures de confinement et le diagnostic, sans demander de journaliser tous les
prompts. Indiquer les tests de non-régression nécessaires.
