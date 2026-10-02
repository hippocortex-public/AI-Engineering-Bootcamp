# Catalogue de métriques — S5 J5

| Nom | Type | Description | Seuil initial recommandé |
|---|---|---|---|
| `request_count` | counter | nombre total de requêtes | aucun |
| `error_count` | counter | nombre de réponses HTTP en erreur | surveiller variation |
| `error_rate` | gauge | erreurs / requêtes | > 5 % |
| `avg_latency_ms` | gauge | latence moyenne | contexte dépendant |
| `p95_latency_ms` | gauge | 95e percentile | > 3000 ms |
| `prompt_tokens` | counter | tokens d’entrée | surveiller hausse |
| `completion_tokens` | counter | tokens de sortie | surveiller hausse |
| `estimated_cost_usd` | counter | coût estimé cumulé | budget projet |
| `empty_response_count` | counter | réponses vides | > 10 sur fenêtre courte |
| `cache_hit_rate` | gauge | efficacité cache | selon objectif |
