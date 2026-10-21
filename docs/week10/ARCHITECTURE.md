# Architecture — Atelier NLP S10

## Décision

Utiliser une baseline entraînable et traçable avant un modèle Transformer. Séparer les tâches et leurs contrats, puis assembler les sorties sans autoriser d’effet métier.

| Composant | Méthode exécutée | Contrat et limite |
|---|---|---|
| Classification | TF-IDF + SGD log_loss | Trois classes, probabilités non calibrées |
| Extraction | Regex et Decimal | Valeur, statut, preuve; mention sans causalité |
| Résumé | Centralité TF-IDF de phrases | Extractif, pas évaluation de factualité |
| NER | Gazetteer + email regex | Noms connus, spans exacts, pas anonymisation |
| Adaptation | partial_fit de la tête | Représentation figée, pas LoRA |
| Embedding spécialisé | Projection NCA | Pertinence par thème, pas qrels sémantiques |
| Intégration | Agrégation et requires_review | Aucune action externe |

## Partitions et provenance

Le vectoriseur et la tête initiale utilisent train. Seule la tête est poursuivie sur adapt. Validation choisit epochs et seuils; test mesure après sélection. Les id, groupes et doublons normalisés sont vérifiés. Les templates fictifs restent simples et leur séparation ne prouve pas une indépendance comparable à des incidents réels.

La projection NCA n’utilise que les textes et labels train. L’index de voisins contient train; les requêtes sont test. La règle de pertinence est la classe, donc douze documents train sont pertinents par requête et le Recall@3 maximal vaut 0,25.

## Revue et confiance

requires_review combine abstention de classe, ticket_id absent/ambigu et conflit de champ. Cette règle n’authentifie personne et ne contrôle pas une ressource externe. Une application réelle doit ajouter les droits, la validation d’action et le cycle de décision des semaines précédentes.

Les entités et preuves conservent des indices de caractères Python, end exclusif. Le masquage partiel change les positions du texte résultant : ne pas réutiliser les anciens offsets sur ce résultat.

## Artefacts

Le classifieur est exporté en JSON : vocabulaire, IDF, coefficients, intercepts, classes, seuil et provenance. La relecture contrôle formes, finitude et cohérence de hash, puis reproduit le calcul one-vs-rest. Aucun pickle n’est chargé. Une empreinte sans chaîne de confiance ne prouve pas l’auteur de l’artefact.

## Extensions et raccords

LoRA est fourni comme script optionnel sur un modèle BERT local, non exécuté. Il ne remplace pas la baseline et n’entraîne pas sur le test. Le module S10 n’écrit aucun export partagé; raccorder explicitement process à votre API/agent après alignement du schéma.

## Propositions d’amélioration

Corpus réservé représentatif, traitement des négations, relations entre entités, NER apprise, calibration, données de rappel pour éviter l’oubli et vraie évaluation de pertinence. Chaque ajout doit conserver les preuves de séparation et les limites des métriques.
