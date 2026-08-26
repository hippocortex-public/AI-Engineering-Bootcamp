# Lab — Coordinateur multi-agent

## Objectif

Implémenter un coordinateur multi-agent déterministe et testable.

Le lab ne dépend d'aucune API externe.  
Les agents sont simulés par des classes Python pour isoler la logique d'orchestration.

## Fichiers

```text
multi_agent_coordinator.py
test_multi_agent_coordinator.py
```

## Exécution

Depuis ce dossier :

```bash
python multi_agent_coordinator.py
python test_multi_agent_coordinator.py
```

## Ce que le lab démontre

- registre d'agents ;
- sélection d'agents par domaine ;
- plan de coordination ;
- exécution des spécialistes ;
- contexte minimal ;
- détection de conflit ;
- reviewer conditionnel ;
- trace JSON ;
- sortie structurée.

## Extension proposée

Ajouter un `legal_agent` et une politique de revue spécifique pour les tâches contractuelles.
