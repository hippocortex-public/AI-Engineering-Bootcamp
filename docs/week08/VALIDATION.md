# Validation — Semaine 8

Date : 20 octobre 2026. Python exécuté : 3.12.14.

| Contrôle | Résultat |
|---|---|
| Sept journées, sources et corrigés requis | Complets |
| Notebooks élève / enseignant | 7 + 7 |
| Cellules Python exécutées | 23 réussies |
| Régénération Markdown vers notebooks | Octets identiques |
| Tests du moteur J1 conservé | 14 réussis |
| Tests AI Ops et CLI | 31 réussis |
| Scénarios J2 à J7 | Exécutés |
| CLI : acceptation / refus / preuve invalide | Codes 0 / 1 / 2 vérifiés |
| Liens relatifs des journées | Résolus |
| Fichiers J1 repris, dont notebooks | 28 fichiers identiques octet par octet |
| Rapports de référence | Recalculés depuis les fixtures |

## Méthode

`scripts/validate_week08.py` vérifie la structure, régénère les notebooks, compare leurs octets, exécute les cellules de code séquentiellement dans un namespace neuf par notebook, lance les labs et les deux suites unittest. La structure JSON nbformat 4.5 est vérifiée par le script. Aucun kernel Jupyter ni validation par la bibliothèque nbformat n’a été utilisé.

Les tests couvrent les refus critiques et la couverture, les essais manquants/dupliqués/inconnus, les mesures non finies ou négatives, les protocoles incompatibles, le calcul des coûts et du cache, les timeouts conservés, les budgets réservés et les règlements idempotents, les champs de télémétrie, les approbations obsolètes/expirées, les permissions positives/négatives et les codes CLI. Les tests d’origine J1 restent inchangés.

## Ce que ces contrôles ne prouvent pas

Aucun modèle ou fournisseur réel n’a été interrogé. Les latences et coûts sont synthétiques. Les sorties de qualité de J1 sont réutilisées pour les répétitions; ce ne sont pas des générations indépendantes. Les tests de sécurité vérifient un contrôleur sur fixtures, sans authentification réelle ni exécution d’outil. Aucun SDK OpenTelemetry, charge concurrente, ledger distribué, canary, déploiement ou rollback réel n’est mis en œuvre.

La vue HTML est un rapport statique autonome généré depuis les mêmes JSON. Son contenu et sa structure sont contrôlés; aucun rendu visuel dans un navigateur n’a été effectué dans cet environnement.

Le code ne remplace pas les composants des semaines précédentes et ne certifie pas leur intégration en production. Les raccords et améliorations sont explicités dans ARCHITECTURE.md et RUNBOOK.md.

## Reproduire

```bash
python3 scripts/validate_week08.py
python3 scripts/make_week08_reports.py
```
