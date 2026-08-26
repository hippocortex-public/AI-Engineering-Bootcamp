# Review formateur — MCP Client

## Résumé pédagogique

Cette journée est le pendant client du jour 3.

Les apprenants doivent comprendre qu'un serveur MCP expose des capacités, mais que le client est la couche qui rend ces capacités utilisables par un agent en production.

## Points à vérifier

- L'apprenant distingue agent, client MCP, serveur MCP et tool métier.
- L'apprenant sait expliquer `initialize`, `tools/list` et `tools/call`.
- L'apprenant comprend pourquoi la validation locale est utile.
- L'apprenant sait construire une registry d'outils dynamique.
- L'apprenant sait expliquer les risques du cache.
- L'apprenant sait justifier le blocage d'une action sensible.

## Erreurs fréquentes

1. Confondre client MCP et agent.
2. Mettre la planification dans le client.
3. Ne pas valider les arguments.
4. Ne pas tracer les appels.
5. Considérer le cache comme une source de vérité permanente.
6. Laisser un tool sensible s'exécuter sans approbation.

## Questions de relance

- Que se passe-t-il si le serveur change son schéma ?
- Où placerais-tu une politique d'autorisation ?
- Comment testerais-tu ce client sans serveur réel ?
- Comment adapterais-tu ce client pour plusieurs serveurs MCP ?
- Comment masquerais-tu les secrets dans les traces ?

## Barème indicatif

| Critère | Points |
|---|---:|
| Séparation des responsabilités | 4 |
| Initialisation et découverte | 4 |
| Validation locale | 4 |
| Gestion d'erreurs | 3 |
| Sécurité | 3 |
| Traces | 2 |
| Total | 20 |
