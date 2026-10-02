# Review — Semaine 5 Jour 5

## Points à valider

L’apprenant doit être capable d’expliquer :

- pourquoi le monitoring IA dépasse le simple statut HTTP ;
- comment construire un snapshot de métriques ;
- pourquoi le P95 est plus utile que la moyenne pour diagnostiquer les lenteurs ;
- comment estimer un coût LLM ;
- pourquoi les prompts bruts ne doivent pas être loggés ;
- comment transformer un seuil en alerte actionnable.

## Erreurs fréquentes

### Confondre logs et métriques

Un log décrit un événement. Une métrique agrège une mesure. Les deux sont nécessaires mais ne répondent pas au même besoin.

### Oublier les coûts

Dans une application IA, le coût peut être une régression aussi importante qu’une erreur technique.

### Logger trop de données

Un monitoring non filtré peut exposer des secrets ou données personnelles. La redaction doit faire partie du design initial.

### Surveiller uniquement la moyenne

Une moyenne acceptable peut masquer une mauvaise expérience pour une minorité d’utilisateurs. Le P95 est indispensable.

### Créer des alertes non actionnables

Une alerte sans runbook crée du bruit. Une alerte doit dire quoi vérifier.

## Questions de consolidation

1. Quel signal permet de détecter une réponse vide malgré un `200 OK` ?
2. Comment calculer un taux d’erreur ?
3. Pourquoi faut-il corréler les logs avec un `request_id` ?
4. Comment diagnostiquer une hausse de coût ?
5. Pourquoi tester le monitoring ?

## Extension possible

La suite logique de cette journée est d’intégrer :

- Prometheus ;
- Grafana ;
- OpenTelemetry ;
- dashboards par route ;
- alertes Slack ou PagerDuty ;
- évaluation continue de qualité IA ;
- budgets par tenant.

## Propositions d'amélioration

Ces propositions ne modifient pas les spécifications figées du bootcamp.

- Ajouter plus tard un module optionnel Prometheus dans les labs avancés.
- Ajouter un dashboard Grafana préconfiguré en semaine 8.
- Ajouter une comparaison entre monitoring applicatif et observabilité distribuée.
