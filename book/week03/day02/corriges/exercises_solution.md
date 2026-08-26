# Corrigé — Exercices — Coordination multi-agents

## Exercice 1 — Identifier les rôles

1. Choisir entre support et billing : **router**.
2. Vérifier une promesse interdite : **reviewer**.
3. Transformer trois analyses locales : **synthesizer**.
4. Décider d'un traitement parallèle : **manager**.
5. Transférer vers juridique : **handoff**.

## Exercice 2 — Sélection d'agents

1. Facturation double + réponse client :
   - `billing_agent`
   - `support_agent`
   - éventuellement `reviewer_agent` si remboursement ou client entreprise.

2. Erreur 500 sur API de paiement :
   - `engineering_agent`
   - `billing_agent`
   - `reviewer_agent` si impact client ou risque élevé.

3. Utilisateur sans accès :
   - `security_agent`
   - `support_agent`
   - éventuellement `engineering_agent` si bug technique.

4. Bug exposant des données :
   - `engineering_agent`
   - `security_agent`
   - `support_agent`
   - `reviewer_agent`.

5. Résumé note produit sans risque :
   - `product_agent`
   - éventuellement `support_agent` si réponse utilisateur attendue.

## Exercice 3 — Contexte minimal

### billing_agent

```text
task_id
objectif: vérifier la facture
montant attendu: 120 €
montant facturé: 1 200 €
demande client: remboursement immédiat
contrainte: ne pas promettre de remboursement sans validation
risk_level: medium/high
```

### engineering_agent

```text
task_id
objectif: analyser l'erreur API mentionnée
indice: erreur API observée hier
lien potentiel: facturation incorrecte
contrainte: produire une hypothèse technique vérifiable
risk_level: medium
```

### support_agent

```text
task_id
objectif: préparer une réponse client
client: entreprise
sentiment: mécontent
faits confirmés: facture contestée, erreur API mentionnée
contrainte: empathie sans engagement non autorisé
risk_level: high
```

### reviewer_agent

```text
task_id
objectif: vérifier cohérence et risque
résultats billing/support/engineering
risques: remboursement, client entreprise, incident possible
contrainte: signaler promesses interdites et incertitudes
```

## Exercice 4 — Détection de conflit

1. Oui, il y a conflit : `resolved` vs `unresolved`.
2. Le coordinateur doit déclencher une revue ou demander une observation supplémentaire.
3. La réponse à éviter est : "Le problème est corrigé et tout fonctionne", car elle contredit le signal client.

## Exercice 5 — Politique de revue

Exemple de règle :

```python
requires_review = (
    risk_level == "high"
    or has_conflict
    or contains_sensitive_action
    or missing_required_information
    or external_enterprise_response
)
```

## Exercice 6 — Trace JSON minimale

```json
{
  "task_id": "task-42",
  "selected_agents": ["support_agent", "billing_agent"],
  "events": [
    {"type": "task_received", "task_id": "task-42"},
    {"type": "agents_selected", "agents": ["support_agent", "billing_agent"]},
    {"type": "agent_completed", "agent": "support_agent"},
    {"type": "agent_completed", "agent": "billing_agent"},
    {"type": "conflict_check", "conflicts": []},
    {"type": "final_answer_created"}
  ],
  "review_performed": false,
  "status": "completed"
}
```

## Exercice 7 — Amélioration du lab

Une solution possible :

```python
legal_agent = SpecialistAgent(
    name="legal_agent",
    domains=["legal"],
    default_status="caution",
    summary_template="Legal review required for task {task_id}."
)
```

Puis ajouter `legal_agent` au registre.

Test attendu :

```python
def test_legal_agent_is_selected_and_high_risk_triggers_review():
    registry = build_default_registry()
    registry.register(SpecialistAgent(
        name="legal_agent",
        domains=["legal"],
        default_status="caution",
        summary_template="Legal review required for task {task_id}."
    ))
    coordinator = MultiAgentCoordinator(registry)
    task = CoordinationTask(
        task_id="legal-1",
        objective="Review contractual wording",
        domains=["legal"],
        risk_level="high",
        constraints=[]
    )
    result = coordinator.run(task)
    assert "legal_agent" in result.selected_agents
    assert result.review_performed is True
    assert any(item.agent == "legal_agent" for item in result.observations)
```
