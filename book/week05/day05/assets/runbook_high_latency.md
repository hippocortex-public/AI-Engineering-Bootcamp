# Runbook — Latence élevée

## Signal

Alerte `high_p95_latency`.

## Diagnostic

1. Vérifier si la latence concerne toutes les routes ou seulement `/chat`.
2. Comparer P50, P95 et P99.
3. Vérifier la taille moyenne des prompts.
4. Vérifier le nombre d’appels d’outils.
5. Vérifier les retries fournisseur.
6. Vérifier Redis et PostgreSQL.
7. Vérifier le dernier déploiement.
8. Vérifier les changements de modèle ou de configuration.

## Mitigations possibles

- réduire la fenêtre de contexte ;
- activer ou augmenter le cache ;
- désactiver temporairement les outils coûteux ;
- basculer vers un modèle plus rapide ;
- rollback applicatif ;
- limiter les requêtes par utilisateur.
