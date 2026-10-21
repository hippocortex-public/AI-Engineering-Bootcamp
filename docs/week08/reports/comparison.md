# Rapport de supervision synthétique — 20 octobre 2026

Données fabriquées; aucun fournisseur, outil externe ou déploiement exécuté.

| Indicateur | Baseline | Candidat |
|---|---|---|
| Décision locale | ACCEPTÉE | REFUSÉE |
| Qualité J1 | 83.33% | 91.67% |
| Cas critiques | True | False |
| p95 automatisé (ms) | 601 | 461 |
| Maximum (ms) | 609 | 2200 |
| Erreurs techniques | 0.00% | 2.78% |
| Coût utile USD synthétique | 0.002028 | 0.00156375 |
| Contrôles refusés | aucun | quality |

Le candidat est plus rapide et moins cher, mais la régression critique c09 bloque quality. Les 36 tentatives par version réutilisent les 12 résultats de qualité de J1; ce ne sont pas 36 générations indépendantes.
