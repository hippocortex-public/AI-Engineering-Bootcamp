# Semaine 8 — AI Engineering Ops

Construire une décision de livraison à partir de preuves de qualité, de performance, de coût, de gouvernance et de permissions.

| Jour | Thème | Livrable principal |
|---|---|---|
| J1 | Évaluation | Comparaison appariée et veto critique |
| J2 | Benchmarks | Quantiles, maximum, erreurs et protocole |
| J3 | Observabilité | Journaux corrélés, métriques et SLI de lot |
| J4 | Coûts | Coût utile et réservation de budget |
| J5 | Gouvernance | Manifeste lié à la configuration |
| J6 | Sécurité | Contrôleur de permissions testé |
| J7 | Projet de supervision | Décision intégrée et preuves |

La roadmap du plugin prescrit ces six thèmes et le projet de supervision. Le découpage J2 à J7 détaille les thèmes sans modifier la roadmap. J1 reprend intégralement l’archive déjà livrée, y compris les deux notebooks, les fixtures, le cours et les corrigés.

## Parcours

Commencer par [QUICKSTART.md](QUICKSTART.md), puis `book/week08/day01/README.md`. Si J1 est déjà étudié, reprendre directement à J2. J1 conserve sa durée d’origine de 4 h 30; pour J2 à J7, prévoir une heure pour l’essentiel et 2 à 3 heures pour l’unité complète. Les entretiens et challenges peuvent être répartis sur des sessions supplémentaires.

Les labs sont exécutables sans clé LLM, sans réseau et sans infrastructure. Les sorties, observations de performance, identités et prix sont synthétiques. Les résultats démontrent le protocole local; ils ne mesurent aucun fournisseur réel.

## Fil rouge

Le candidat de J1 passe de 10/12 à 11/12, mais échoue sur c09, cas critique. Les nouveaux labs lui donnent aussi un meilleur p95 et un coût utile inférieur. La décision finale reste un refus. Une économie ou une moyenne plus élevée ne compense pas une exigence critique violée.

## Intégration sans perte

Décompresser dans un dossier temporaire puis copier les sous-arbres `book/week08`, `notebooks/week08`, `examples/week08`, `tests/week08` et `docs/week08` vers leurs homologues. Ajouter les scripts dont le nom contient week08. Vérifier les éventuelles modifications personnelles de J1 avant de copier les fichiers : le paquet conserve la version déjà livrée, mais ne connaît pas vos éditions locales.

Aucun README racine, ROADMAP, pyproject, requirements global, workflow CI, mini_framework/__init__.py ou ai_platform/__init__.py n’est remplacé. Le module commun S8 appelle le moteur local de J1; il n’affirme pas être déjà branché sur votre backend S5 ou le workflow n8n S7.

Consulter [VALIDATION.md](VALIDATION.md) pour les contrôles réalisés et [ARCHITECTURE.md](ARCHITECTURE.md) pour les frontières du projet. Les rapports de référence sont dans `docs/week08/reports`.

## Propositions d’amélioration

Collecteur de mesures réelles, adaptateur LLM évalué, SDK OpenTelemetry, ledger durable, identité vérifiée, approbations signées et rollback en environnement isolé. Ces extensions ne sont pas présentées comme implémentées et ne modifient aucune spécification gelée.
