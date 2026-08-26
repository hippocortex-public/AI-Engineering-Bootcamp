# Corrigé — Challenge — Jour 6

## Implémentation de référence

```python
def build_for_agent(agent_name, items, policy):
    selected = []
    dropped = []
    total_tokens = 0

    for item in items:
        targets = item.get("target_agents", [])
        if targets and agent_name not in targets:
            dropped.append({"id": item["id"], "reason": "wrong_target_agent"})
            continue

        if item.get("visibility") == "private" and agent_name not in item.get("target_agents", []):
            dropped.append({"id": item["id"], "reason": "private_not_allowed"})
            continue

        tokens = item.get("tokens", len(item.get("content", "").split()))
        if total_tokens + tokens > policy["max_tokens"]:
            dropped.append({"id": item["id"], "reason": "budget_exceeded"})
            continue

        selected.append(item)
        total_tokens += tokens

    return {
        "agent": agent_name,
        "selected": selected,
        "dropped": dropped,
        "total_tokens": total_tokens,
    }
```

## Exemple `billing_agent`

Le `billing_agent` doit recevoir :

- son instruction système ;
- l’état de facture ;
- la politique de facturation ;
- les outils de lecture facture.

Il ne doit pas recevoir :

- notes privées sécurité ;
- outils destructifs non nécessaires ;
- traces internes du router.

## Exemple `security_agent`

Le `security_agent` peut recevoir :

- note de sécurité ;
- extrait du ticket ;
- règles de traitement des secrets ;
- outils de validation ou d’escalade.

Il ne doit pas recevoir automatiquement :

- détails de facturation inutiles ;
- préférences utilisateur sans rapport ;
- historique non lié.

## Tests attendus

1. `billing_agent` ne reçoit pas `security_note`.
2. `security_agent` reçoit `security_note` si elle lui est explicitement destinée.
3. Le budget est respecté.
4. Les éléments hors cible sont tracés.
5. Les emails sont réduits.
6. Le rendu final contient les IDs de sources.

## Réponse à la question de réflexion

Le contexte du `security_agent` peut contenir des hypothèses, secrets, alertes ou diagnostics qui ne sont pas utiles au traitement facturation. Le rendre visible au `billing_agent` peut exposer des informations sensibles et biaiser la réponse métier.
