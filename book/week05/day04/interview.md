# Questions d’entretien — Semaine 5 Jour 4

## Questions courtes

1. Pourquoi PostgreSQL est-il souvent préférable à Redis pour l’historique conversationnel durable ?
2. Quelles données d’un agent IA doivent être conservées pour l’audit ?
3. Pourquoi ne faut-il pas tout stocker dans une seule colonne JSONB ?
4. À quoi sert une transaction dans un tour de conversation IA ?
5. Quelle est la différence entre un message assistant et un agent run ?
6. Pourquoi enregistrer les appels d’outils ?
7. Quel index proposeriez-vous pour récupérer les messages d’une conversation ?
8. Pourquoi un `tenant_id` est-il important ?
9. Que signifie idempotence dans une API IA ?
10. Quel est le rôle du repository pattern ?

## Questions de conception

11. Vous devez concevoir la base de données d’un assistant IA B2B. Quelles tables créez-vous en priorité ?
12. Comment stockeriez-vous les métadonnées variables d’un appel LLM ?
13. Comment retrouveriez-vous les 50 derniers runs échoués ?
14. Comment calculeriez-vous la latence moyenne par modèle ?
15. Comment éviteriez-vous les doublons lors d’un retry réseau ?

## Cas pratique

Vous rejoignez une équipe qui stocke seulement les messages utilisateur et assistant dans une table `messages`. Aucun run, aucun tool call, aucun prompt version et aucune évaluation ne sont conservés.

Expliquez :

- les risques de cette approche ;
- le schéma minimal à ajouter ;
- l’ordre de migration ;
- les bénéfices attendus pour le monitoring et le debug.
