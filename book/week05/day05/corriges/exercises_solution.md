# Corrigé — Exercices

## Exercice 1 — Identifier les métriques

1. Lenteur ressentie par les utilisateurs : `p95_latency_ms`, éventuellement `p99_latency_ms`.
2. Facture LLM en hausse : `estimated_cost_usd`, `total_tokens`, `prompt_tokens`, `completion_tokens`.
3. Réponse vide avec `200 OK` : `empty_response_count` et taux de réponses vides.
4. Erreurs après déploiement : `error_rate`, `error_count`, distribution des `status_code`.
5. Prompts plus longs : `prompt_tokens`, taille moyenne du prompt, éventuellement longueur de contexte.

## Exercice 2 — Calculer un coût estimé

Formule :

```text
coût = 1500 / 1000 * 0.002 + 400 / 1000 * 0.006
```

Calcul :

```text
coût = 1.5 * 0.002 + 0.4 * 0.006
coût = 0.003 + 0.0024
coût = 0.0054 USD
```

Le coût estimé est donc **0.0054 USD**.

## Exercice 3 — Définir des SLO

Exemples acceptables :

- Latence : 95 % des requêtes `/chat` doivent répondre en moins de 3 secondes sur une fenêtre de 15 minutes.
- Erreur : le taux d’erreur HTTP 5xx doit rester inférieur à 1 % sur une fenêtre de 15 minutes.
- Coût : le coût total estimé ne doit pas dépasser 50 USD par jour pour l’environnement production.

## Exercice 4 — Redaction

Message filtré :

```text
Bonjour, mon email est [REDACTED_EMAIL] et ma clé API est [REDACTED_SECRET].
```

L’objectif est de conserver l’utilité du log sans exposer de donnée sensible.

## Exercice 5 — Lire un snapshot de métriques

Snapshot :

```json
{
  "error_rate": 0.07,
  "p95_latency_ms": 4200,
  "estimated_cost_usd": 83.5
}
```

Alertes déclenchées :

- `high_error_rate`, car `0.07 > 0.05` ;
- `high_p95_latency`, car `4200 > 3000` ;
- `high_estimated_cost`, car `83.5 > 75`.

On peut également surveiller `empty_response_count`, mais aucun seuil n’est fourni dans l’énoncé.

## Exercice 6 — Instrumentation

Exemple de solution :

```python
def record_ai_request(
    metrics_store,
    latency_ms: float,
    status_code: int,
    prompt_tokens: int,
    completion_tokens: int,
    estimated_cost_usd: float,
    empty_response: bool,
) -> None:
    metrics_store.record(
        latency_ms=latency_ms,
        status_code=status_code,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        estimated_cost_usd=estimated_cost_usd,
        empty_response=empty_response,
    )
```

La fonction est volontairement simple : elle délègue la responsabilité d’agrégation au `metrics_store`.

## Exercice 7 — Qualité IA

Signaux simples possibles :

- hausse du nombre de réponses vides ;
- hausse des réponses de fallback ;
- baisse du score d’évaluation automatique ;
- hausse des feedbacks négatifs utilisateurs ;
- hausse des reformulations ;
- réponses trop courtes ou trop longues ;
- incohérence avec des réponses attendues ;
- hausse des refus.
