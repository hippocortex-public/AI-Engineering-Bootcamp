# Corrigé — Exercices

## Exercice 1

1. Valider les arguments d'une fonction → `ToolRegistry`
2. Stocker une préférence utilisateur → `MemoryStore`
3. Détecter une dépendance cyclique → `WorkflowRunner`
4. Enregistrer un appel d'outil → `Tracer`
5. Définir les outils autorisés pour un agent → `AgentSpec`

## Exercice 2

```python
billing_agent = AgentSpec(
    name="billing_agent",
    instructions="Traiter les demandes liées à la facturation, aux factures et aux remboursements.",
    allowed_tools=["classify_ticket", "search_kb", "draft_answer"]
)
```

L'agent ne reçoit pas `issue_refund` dans sa liste d'outils autorisés.

## Exercice 3

`issue_refund` est sensible car il déclenche potentiellement une action financière réelle.

Conditions minimales :

1. identité utilisateur et commande vérifiées ;
2. approbation humaine ou politique automatique explicite.

On peut ajouter :

- limite de montant ;
- journal d'audit ;
- double validation ;
- contrôle anti-fraude.

## Exercice 4

Workflow attendu :

```text
classify → search_policy → risk_review → draft_answer
```

Dépendances :

```text
search_policy dépend de classify
risk_review dépend de search_policy
draft_answer dépend de risk_review
```

## Exercice 5

Trace minimale :

- `run.started`
- `memory.lookup`
- `workflow.step.started`
- `tool.call.started`
- `tool.call.completed`
- `workflow.step.completed`
- `run.completed`

En cas d'erreur, ajouter :

- `tool.call.failed`
- `run.failed`
- `guardrail.blocked`

## Exercice 6

1. outil inconnu → `failed`
2. agent inconnu → `failed`
3. outil sensible sans approbation → `blocked`
4. dépendance cyclique → `failed`
5. exécution complète → `completed`

## Exercice 7

Extension possible :

- ajouter un adaptateur HTTP FastAPI ;
- ajouter un store mémoire persistant ;
- ajouter un exporter de traces ;
- ajouter un système de configuration YAML ;
- ajouter des quotas par utilisateur.

Ces extensions ne changent pas le contrat du framework. Elles ajoutent des adaptateurs.
