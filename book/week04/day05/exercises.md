# Exercises

## Exercice 1 — Identifier les responsabilités du workflow engine

Pour chaque responsabilité, indique si elle appartient plutôt :

- au workflow engine ;
- au handler ;
- au modèle ;
- au tool registry ;
- à la memory layer.

Responsabilités :

1. déterminer l'ordre des étapes ;
2. appeler une API métier ;
3. stocker une préférence utilisateur durable ;
4. décider si une étape sensible est approuvée ;
5. produire une trace d'exécution ;
6. valider que le graphe n'a pas de cycle ;
7. générer une réponse naturelle ;
8. vérifier que l'outil existe.

## Exercice 2 — Concevoir un workflow

Conçois un workflow de qualification de lead avec les étapes suivantes :

- `classify_lead` ;
- `enrich_company` ;
- `score_lead` ;
- `request_sales_review` ;
- `final_summary`.

Contraintes :

- `enrich_company` dépend de `classify_lead` ;
- `score_lead` dépend de `enrich_company` ;
- `request_sales_review` est sensible ;
- `final_summary` dépend de `score_lead` et de `request_sales_review` ;
- `request_sales_review` ne s'exécute que si le score est supérieur à 80.

Produis la liste des étapes avec leurs dépendances.

## Exercice 3 — Statuts

Associe le statut approprié :

1. une étape a fini sans erreur ;
2. une étape attend une validation humaine ;
3. une étape n'a pas été lancée car sa condition est fausse ;
4. une étape a levé une erreur après tous ses retries ;
5. le workflow a démarré mais n'est pas terminé.

Statuts disponibles :

- `running`
- `completed`
- `failed`
- `blocked`
- `skipped`

## Exercice 4 — Lire une trace

On observe la trace suivante :

```json
[
  {"event": "workflow.started"},
  {"step": "plan", "event": "step.started", "payload": {"attempt": 1}},
  {"step": "plan", "event": "step.failed"},
  {"step": "plan", "event": "step.retry_scheduled"},
  {"step": "plan", "event": "step.started", "payload": {"attempt": 2}},
  {"step": "plan", "event": "step.completed"},
  {"event": "workflow.finished", "payload": {"status": "completed"}}
]
```

Questions :

1. Combien de tentatives l'étape `plan` a-t-elle utilisées ?
2. Le workflow a-t-il échoué ?
3. Que peut-on conclure sur `max_retries` ?
4. Pourquoi cette trace est-elle utile en production ?

## Exercice 5 — Implémentation guidée

Dans le lab :

1. exécute `workflow_engine_lab.py` ;
2. observe le JSON produit ;
3. retire l'approbation `refund` ;
4. relance le workflow ;
5. explique pourquoi le statut devient `blocked`.

## Exercice 6 — Extension

Ajoute une étape `notify_customer` après `final_answer`.

Contraintes :

- dépend de `final_answer` ;
- handler `notify_customer` ;
- sensible ;
- doit produire un objet `{ "sent": true }` si approuvé.

Explique les tests à ajouter.
