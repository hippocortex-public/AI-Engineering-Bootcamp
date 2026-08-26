# Challenge — Instrumenter un assistant support

## Contexte

Tu disposes d'un mini-framework avec :

- un agent ;
- un registre d'outils ;
- une couche mémoire ;
- un workflow engine.

Tu dois concevoir l'observabilité d'un assistant support qui peut :

1. classifier une demande ;
2. récupérer le profil utilisateur ;
3. rechercher un ticket ;
4. proposer une action ;
5. demander une approbation humaine si l'action est sensible ;
6. produire une réponse finale.

## Travail demandé

Crée une conception technique contenant :

1. l'arbre de spans ;
2. les événements importants ;
3. les métriques ;
4. les règles de redaction ;
5. les statuts possibles ;
6. un exemple d'export JSON ;
7. trois alertes opérationnelles.

## Contraintes

- l'email utilisateur ne doit jamais apparaître en clair ;
- les arguments d'outil sensibles doivent être masqués ;
- un outil échoué doit créer un span `failed` ;
- une action bloquée par guardrail doit être visible ;
- la trace complète peut être `completed` si l'agent produit une réponse sûre.

## Critères d'acceptation

Le challenge est réussi si :

- le modèle distingue bien trace/span/event/metric ;
- le design est exploitable en production ;
- les données sensibles sont protégées ;
- les erreurs ne sont pas masquées ;
- les décisions agentiques restent auditables.
