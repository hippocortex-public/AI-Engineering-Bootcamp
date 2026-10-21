# Semaine 10 — NLP appliqué

Construire un atelier NLP sur des tickets d’exploitation : apprendre, extraire, résumer, reconnaître des entités, adapter et comparer.

| Jour | Thème | Livrable principal |
|---|---|---|
| J1 | Classification | TF-IDF + tête linéaire entraînés |
| J2 | Extraction | Valeurs, statuts et preuves source |
| J3 | Résumé | Phrases exactes sous budget |
| J4 | NER | Spans typés et évaluation stricte |
| J5 | Fine-tuning léger | Adaptation réelle d’une tête figée en représentation |
| J6 | Embeddings spécialisés | Projection supervisée NCA |
| J7 | Projet intégré | Analyse de ticket, revue et artefacts |

La roadmap prescrit ces six thèmes et le projet NLP. Le découpage journalier détaille ces thèmes sans modifier les spécifications. Prévoir une heure par jour pour l’essentiel ou 2 à 3 heures pour l’unité complète. L’installation de l’environnement et le lab LoRA ajoutent un temps distinct.

## Nature des méthodes

Le parcours entraîne réellement des modèles scikit-learn : vocabulaire/IDF, tête de classification, adaptation de cette tête et projection NCA. L’extraction et la NER sont des baselines à règles; le résumé sélectionne des phrases selon une centralité TF-IDF. Aucune prédiction de classification n’est préfabriquée et aucun modèle n’est téléchargé par les labs obligatoires.

Le corpus reste fictif : 72 tickets, quatre exemples annotés pour les traitements de texte et trois exemples hors domaine ou ambigus. Les partitions sont 36 train, 12 adapt, 12 validation et 12 test. Le protocole vérifie la séparation des groupes et refuse les doublons exacts normalisés; il ne détecte pas automatiquement tous les quasi-doublons sémantiques.

## Progression

Commencer par [QUICKSTART.md](QUICKSTART.md), puis `book/week10/day01/README.md`. J1 apprend une baseline, J5 adapte sa tête et J6 apprend une géométrie de voisinage. Les notebooks élèves et enseignants se trouvent sous notebooks/week10 et notebooks/week10/teacher.

Le lab LoRA de `examples/week10/optional` est séparé et non exécuté dans la validation standard. Il utilise un modèle BERT local et de vrais adaptateurs PEFT, mais ne fournit aucun score de fine-tuning Transformer validé ici.

## Résultats et limites

La tête adaptée change de poids sans gagner de F1 sur le petit test facile. La projection NCA améliore le voisinage par catégorie dans l’environnement de référence. Les rapports conservent ces résultats avec leur protocole, sans généraliser à des tickets réels. Voir docs/week10/reports/comparison.md et [VALIDATION.md](VALIDATION.md).

## Intégration au dépôt

Copier les sous-arbres book/week10, notebooks/week10, examples/week10, tests/week10 et docs/week10 vers leurs homologues, puis ajouter les scripts dédiés week10. Vérifier vos éventuels fichiers S10 existants avant remplacement.

Aucun fichier racine partagé, spécification, workflow CI, mini_framework/__init__.py ou ai_platform/__init__.py n’est remplacé. Les dépendances restent dans examples/week10/requirements.txt. Le module ne prétend pas être déjà branché à votre API ou vos agents existants.

## Propositions d’amélioration

Collecter un corpus représentatif réservé, annoter négations et relations, apprendre une NER sur noms inconnus, calibrer la revue hors distribution, comparer une synthèse générative et exécuter LoRA si un besoin le justifie. Chaque expérience demande un protocole et des preuves distincts; elle ne modifie pas la roadmap.
