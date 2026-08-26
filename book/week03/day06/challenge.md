# Challenge — Jour 6 — Construire un Context Builder multi-agent

## Contexte

Tu travailles sur une plateforme d’assistants internes.

La plateforme contient trois agents :

- `router_agent` ;
- `billing_agent` ;
- `security_agent`.

Chaque agent ne doit recevoir que le contexte nécessaire à son rôle.

## Objectif

Construire un `ContextBuilder` capable de produire un contexte différent pour chaque agent.

## Contraintes

Le système doit :

1. accepter une liste d’éléments de contexte ;
2. filtrer selon l’agent cible ;
3. respecter un budget de tokens ;
4. exclure les éléments privés non autorisés ;
5. réduire les emails et téléphones ;
6. conserver une trace des éléments supprimés ;
7. produire un rendu lisible pour modèle ;
8. être testé.

## Données d’entrée minimales

```json
[
  {
    "id": "system_router",
    "kind": "system",
    "content": "Tu routes les demandes vers le bon spécialiste.",
    "priority": 100,
    "visibility": "public",
    "target_agents": ["router_agent"]
  },
  {
    "id": "invoice_state",
    "kind": "state",
    "content": "invoice_id=F-392 customer=ACME",
    "priority": 95,
    "visibility": "shared",
    "target_agents": ["billing_agent"]
  },
  {
    "id": "security_note",
    "kind": "memory",
    "content": "Suspicion de secret exposé dans le ticket.",
    "priority": 90,
    "visibility": "private",
    "target_agents": ["security_agent"]
  }
]
```

## Attendu

Tu dois produire :

- une fonction `build_for_agent(agent_name, items, policy)` ;
- un exemple pour `billing_agent` ;
- un exemple pour `security_agent` ;
- au moins quatre tests unitaires.

## Question de réflexion

Pourquoi le contexte du `security_agent` ne doit-il pas être automatiquement visible par le `billing_agent` ?
