# Challenge — Mini workflow de diagnostic IA

## Objectif

Construire un workflow de diagnostic pour une application IA qui reçoit une alerte de production.

## Scénario

Une plateforme IA reçoit une alerte :

```json
{
  "service": "support-agent-api",
  "error_rate": 0.12,
  "latency_p95_ms": 4200,
  "recent_deploy": true
}
```

Le workflow doit :

1. classifier la sévérité ;
2. collecter le contexte ;
3. proposer une hypothèse ;
4. décider si un rollback est recommandé ;
5. demander une approbation humaine avant rollback ;
6. produire un résumé final.

## Contraintes

- `classify_severity` est la première étape ;
- `collect_context` dépend de `classify_severity` ;
- `hypothesize_root_cause` dépend de `collect_context` ;
- `rollback` dépend de `hypothesize_root_cause` ;
- `rollback` est sensible ;
- `rollback` ne s'exécute que si `recent_deploy == true` et `severity == critical` ;
- `final_summary` dépend de `hypothesize_root_cause` et de `rollback`.

## Travail demandé

1. Définir le workflow.
2. Implémenter les handlers.
3. Ajouter une condition `should_rollback`.
4. Exécuter une fois sans approbation.
5. Exécuter une fois avec approbation.
6. Comparer les traces.
7. Ajouter au moins quatre tests.

## Critères de réussite

Le challenge est réussi si :

- le graphe est valide ;
- l'étape de rollback est bloquée sans approbation ;
- l'étape de rollback s'exécute avec approbation ;
- la synthèse finale distingue les cas rollback et non rollback ;
- la trace permet d'expliquer la décision.
