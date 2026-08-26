# Corrections — Exercises

## Exercice 1

1. déterminer l'ordre des étapes — workflow engine ;
2. appeler une API métier — handler, éventuellement via tool registry ;
3. stocker une préférence utilisateur durable — memory layer ;
4. décider si une étape sensible est approuvée — workflow engine avec politique d'approbation ;
5. produire une trace d'exécution — workflow engine / observability ;
6. valider que le graphe n'a pas de cycle — workflow engine ;
7. générer une réponse naturelle — modèle ou handler de réponse ;
8. vérifier que l'outil existe — tool registry.

## Exercice 2

Workflow possible :

```python
WorkflowDefinition(
    name="lead_qualification",
    version="1.0.0",
    steps=[
        WorkflowStep(name="classify_lead", handler="classify_lead"),
        WorkflowStep(name="enrich_company", handler="enrich_company", depends_on=("classify_lead",)),
        WorkflowStep(name="score_lead", handler="score_lead", depends_on=("enrich_company",)),
        WorkflowStep(
            name="request_sales_review",
            handler="request_sales_review",
            depends_on=("score_lead",),
            condition="score_above_80",
            sensitive=True,
        ),
        WorkflowStep(
            name="final_summary",
            handler="final_summary",
            depends_on=("score_lead", "request_sales_review"),
        ),
    ],
)
```

## Exercice 3

1. une étape a fini sans erreur — `completed` ;
2. une étape attend une validation humaine — `blocked` ;
3. une étape n'a pas été lancée car sa condition est fausse — `skipped` ;
4. une étape a levé une erreur après tous ses retries — `failed` ;
5. le workflow a démarré mais n'est pas terminé — `running`.

## Exercice 4

1. `plan` a utilisé deux tentatives.
2. Le workflow n'a pas échoué : il finit en `completed`.
3. `max_retries` est au moins égal à 1.
4. La trace permet de comprendre qu'il y a eu une erreur temporaire, un retry, puis une récupération. En production, cela aide le debugging, les métriques et l'audit.

## Exercice 5

Sans approbation `refund`, le moteur détecte que l'étape est sensible. Il ne l'exécute pas et retourne `blocked`. L'étape finale dépend de `refund`, donc elle est `skipped`.

## Exercice 6

Modification possible :

```python
WorkflowStep(
    name="notify_customer",
    handler="notify_customer",
    depends_on=("final_answer",),
    sensitive=True,
)
```

Tests à ajouter :

- sans approbation, `notify_customer` est `blocked` ;
- avec approbation, l'étape retourne `{ "sent": True }` ;
- si `final_answer` échoue, `notify_customer` est `skipped` ;
- la trace contient `step.blocked` ou `step.completed` selon le cas.
