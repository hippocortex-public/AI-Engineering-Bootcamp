# Exercices

## Exercice 1 — Identifier les métriques

Pour chaque situation, indique la métrique principale à surveiller.

1. Les utilisateurs se plaignent que l’API répond lentement.
2. La facture LLM augmente soudainement.
3. Le service répond `200 OK`, mais produit parfois une réponse vide.
4. Les erreurs augmentent après un déploiement.
5. Les prompts envoyés au modèle deviennent plus longs.

## Exercice 2 — Calculer un coût estimé

On utilise le barème fictif suivant :

```text
input: 0.002 USD / 1000 tokens
output: 0.006 USD / 1000 tokens
```

Une requête consomme :

```text
prompt_tokens = 1500
completion_tokens = 400
```

Calcule le coût estimé de la requête.

## Exercice 3 — Définir des SLO

Propose trois SLO pour une API `/chat` utilisée en production :

- un SLO de latence ;
- un SLO d’erreur ;
- un SLO de coût.

Chaque SLO doit être mesurable.

## Exercice 4 — Redaction

On veut logger le message suivant :

```text
Bonjour, mon email est alice@example.com et ma clé API est sk-live-1234567890abcdef.
```

Propose une version filtrée adaptée aux logs.

## Exercice 5 — Lire un snapshot de métriques

On observe le snapshot suivant :

```json
{
  "request_count": 1000,
  "error_count": 70,
  "error_rate": 0.07,
  "avg_latency_ms": 900,
  "p95_latency_ms": 4200,
  "estimated_cost_usd": 83.5,
  "empty_response_count": 18
}
```

Hypothèses :

- seuil erreur critique : `error_rate > 0.05`
- seuil P95 critique : `p95_latency_ms > 3000`
- seuil coût : `estimated_cost_usd > 75`

Quelles alertes doivent se déclencher ?

## Exercice 6 — Instrumentation

Écris une fonction Python `record_ai_request` qui reçoit :

- `metrics_store`
- `latency_ms`
- `status_code`
- `prompt_tokens`
- `completion_tokens`
- `estimated_cost_usd`
- `empty_response`

La fonction doit enregistrer une requête dans `metrics_store`.

Tu peux supposer que `metrics_store` expose une méthode `record(...)`.

## Exercice 7 — Qualité IA

Donne quatre signaux simples qui permettent de détecter une dégradation de qualité dans une application IA.
