# Semaine 9 — Knowledge Systems

Construire un pipeline documentaire vérifiable : sources → chunks → représentations → index → retrieval → contexte → réponse référencée.

| Jour | Thème | Preuve principale |
|---|---|---|
| J1 | Chunking | Offsets exacts et fenêtres progressives |
| J2 | Embeddings | Géométrie et compatibilité d’espace |
| J3 | Vector store | Persistance, versions et filtre préalable |
| J4 | Hybrid Search | BM25, cosinus et RRF |
| J5 | Reranking | Score de paire et budget de contexte |
| J6 | Mémoire d’agents | Portée, TTL et source courante |
| J7 | Projet RAG | Extraits cités, abstention et métriques |

La roadmap de référence fixe ces six thèmes et le projet RAG. Le découpage en sept journées détaille ces thèmes sans modifier les spécifications. Prévoir une heure par jour pour l’essentiel, ou 2 à 3 heures pour l’unité complète avec entretien et challenge. L’installation des extensions optionnelles ajoute un temps distinct.

## Ce qui fonctionne hors ligne

Les algorithmes de chunking, projection vectorielle lexicale, cosinus, BM25, RRF, reranking heuristique et métriques s’exécutent réellement. SQLite persiste les passages et vecteurs, puis le moteur applique un scan exact dans le tenant demandé. Les mémoires sont séparées des sources et des citations.

La réponse par défaut est extractive : elle reproduit des passages entiers vérifiés. Aucun modèle génératif n’est appelé. L’encodeur hashbow n’est pas un modèle sémantique appris. Le corpus backend/DevOps est fictif et ses valeurs ne décrivent aucun système de production.

## Extensions disponibles

`examples/week09/optional` contient des adaptateurs pour modèles locaux Sentence Transformers/CrossEncoder et un schéma/requête de référence pgvector. Ces éléments n’ont pas été exécutés dans la validation standard; ni poids neuronaux ni serveur PostgreSQL ne sont requis pour le parcours principal.

## Parcours

Commencer par [QUICKSTART.md](QUICKSTART.md), puis `book/week09/day01/README.md`. Les notebooks élèves sont sous notebooks/week09; les enseignants sous notebooks/week09/teacher. Le générateur consolide les Markdown et leurs corrections en deux variantes par journée.

Le projet reprend les préoccupations de S8 — provenance et limites des mesures — sans remplacer ses modules. J6 se concentre sur le cycle de vie et l’invalidation des mémoires; il ne refait pas l’introduction des types de mémoire de S2/S3.

## Intégration

Décompresser dans un répertoire temporaire puis copier `book/week09`, `notebooks/week09`, `examples/week09`, `tests/week09`, `docs/week09` et les scripts dédiés week09 dans leurs homologues du dépôt. Vérifier les éventuels fichiers S9 déjà édités avant de les remplacer.

Aucun fichier racine partagé, spécification, workflow CI, mini_framework/__init__.py ou ai_platform/__init__.py n’est livré en remplacement. Le raccord à votre backend ou agent existant reste explicite : le module reçoit un tenant supposé autorisé mais n’implémente pas de serveur d’authentification.

Les résultats détaillés et rapports sont dans docs/week09/reports. Lire [VALIDATION.md](VALIDATION.md) pour les preuves réalisées et [ARCHITECTURE.md](ARCHITECTURE.md) pour les garanties exactes.

## Propositions d’amélioration

Rattacher les titres aux passages, évaluer des modèles neuronaux sur des paraphrases réservées, mesurer un vrai index ANN, ajouter des droits par document, une purge mémoire, une synthèse LLM évaluée et des métriques opérationnelles. Ces propositions ne changent pas les spécifications et ne sont pas présentées comme déjà implémentées.
