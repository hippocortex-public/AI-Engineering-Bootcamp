# Objectifs pédagogiques

À la fin de ce jour, l'apprenant sera capable de :

1. Expliquer la différence entre historique conversationnel, state de tâche et mémoire durable.
2. Concevoir un contrat de `MemoryStore` indépendant du backend.
3. Isoler la mémoire par utilisateur, tenant, session ou agent.
4. Définir des types de mémoire : `preference`, `fact`, `task_state`, `tool_observation`, `policy`.
5. Appliquer une politique de visibilité : `private`, `shared`, `public`.
6. Implémenter une récupération déterministe et explicable.
7. Gérer l'expiration avec TTL.
8. Ajouter une politique simple de redaction PII.
9. Produire un snapshot JSON restaurable.
10. Intégrer la mémoire dans un runner ou une boucle agentique.

## Compétence AI Engineering ciblée

La compétence centrale est la capacité à transformer la mémoire d'un agent en **composant logiciel testable**, plutôt qu'en accumulation opaque de messages dans un prompt.

## Anti-objectifs

Ce jour ne vise pas encore à construire :

- une base vectorielle ;
- un RAG complet ;
- une mémoire distribuée ;
- un système de gouvernance complet ;
- une persistance PostgreSQL ou Redis.

Ces sujets arrivent plus tard dans le bootcamp.
