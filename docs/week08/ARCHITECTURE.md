# Architecture du projet de supervision S8

## Décision

Conserver le moteur J1 comme source des résultats de qualité et ajouter un module examples/week08 pour les contrôles transverses. Les cinq décisions restent distinctes et sont combinées par une conjonction. Aucun effet de déploiement n’est attaché au résultat.

| Composant | Entrée | Sortie et responsabilité |
|---|---|---|
| evaluation_lab J1 | Dataset et sorties JSONL | Qualité, couverture et refus critiques |
| benchmark | Grille complète des essais | Quantiles, maximum, erreurs, hashes |
| cost_report | Tous les essais et prix fictifs | Coût total et par succès utile |
| govern | Manifeste, configuration et politique | Raisons d’acceptation ou refus |
| run_security | Cas positifs et négatifs | Conformité du contrôleur de permissions |
| assess | Les cinq familles de preuves | Décision locale restrictive |

## Invariants

Une observation absente ou un protocole incompatible bloque le calcul. Un échec critique ne peut pas être compensé par un gain de vitesse ou de coût. Les timeouts restent dans les mesures et les coûts. Une approbation porte sur une configuration précise. Les logs illustratifs utilisent une liste de champs autorisés. Le budget réserve avant l’admission et ne double pas un règlement répété identique.

## Frontières de confiance

Les mesures sont fictives; leur hash n’atteste pas leur origine. Le manifeste est une fixture, pas une preuve d’authentification. Actor, tenant et grant du contrôleur proviennent du banc de test : un raccord réel devrait les résoudre côté serveur depuis des sources de confiance. Le contrôleur n’implémente ni expiration du grant ni anti-rejeu; le moteur durable S7 traite séparément ces aspects d’une décision de publication locale.

Le module de télémétrie produit du JSON illustratif, sans SDK ni export OTLP. Le ledger de budget est en mémoire, mono-processus. Les durées n’ont pas été mesurées par un générateur de charge. Aucun modèle, outil métier ou API externe n’est exécuté.

## Alternatives

Utiliser une plateforme d’évaluation et d’observabilité peut apporter collecte, stockage, visualisation et gouvernance. Le module local conserve ici une petite surface, des règles lisibles et une exécution hors ligne. Il ne cherche pas à reconstruire un collecteur ou un moteur de déploiement.

## Propositions d’amélioration

Raccorder un collecteur authentifié et une provenance vérifiable, mesurer le système réel avec une charge contrôlée, exporter via OpenTelemetry, persister le ledger et les approbations, puis exercer rollback et canary en environnement isolé. Toute extension doit conserver les invariants et ajouter des preuves adaptées.
