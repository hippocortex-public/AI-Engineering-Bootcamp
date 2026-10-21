# Validation — Semaine 9

Date : 20 octobre 2026. Python exécuté : 3.12.14.

| Contrôle | Résultat |
|---|---|
| Journées complètes selon le standard v1.1 | 7 |
| Notebooks élèves / enseignants | 7 + 7 |
| Cellules Python exécutées | 21 réussies |
| Régénération Markdown vers notebooks | Octets identiques |
| Tests unittest | 35 réussis |
| Scénarios de labs | 7 exécutés |
| Liens relatifs des journées | Résolus |
| Rapports de référence | 6 recalculés depuis le corpus |
| Adaptateurs neuronaux optionnels | Syntaxe compilée, non exécutés |
| Schéma pgvector optionnel | Référence documentaire, non exécutée |

## Méthode

`scripts/validate_week09.py` vérifie la structure, régénère les notebooks, compare leurs octets et exécute les cellules séquentiellement dans un namespace neuf par notebook. Il vérifie le JSON nbformat 4.5 et les liens, compile les modules, lance les sept labs et la suite unittest. Aucun kernel Jupyter ni validation par la bibliothèque nbformat n’a été utilisé. L’affichage Mermaid n’a pas été rendu dans un lecteur graphique.

Les tests couvrent fenêtres et offsets Unicode, progression du chunking, invariance de l’encodage entre processus, vecteurs invalides, cosinus, BM25, RRF, métriques calculables à la main, persistance, filtres de tenant avant top-k, incompatibilité de modèles/dimensions, versions, rollback d’ingestion, suppression, citations falsifiées, budget de contexte, mémoire isolée, expiration exacte et invalidation après changement de source. Les codes CLI de réponse, abstention et entrée invalide sont vérifiés.

## Nature des calculs

Les algorithmes de retrieval et la persistance sont exécutés réellement. Le corpus et les questions sont fictifs. HashEmbedding est une projection lexicale signée, pas un modèle sémantique appris. Le reranker est une heuristique de couverture. La réponse finale reproduit des passages; aucune synthèse LLM n’est exécutée.

Le jeu de huit requêtes positives et deux questions hors corpus n’est pas un échantillon représentatif réservé. Le gain de Recall@3 observé sur une paraphrase provient d’un résultat accidentel de projection au rang 3; la réponse extractive s’abstient. Il ne prouve aucune compréhension sémantique. Les rapports conservent ce cas.

## Extensions non validées à l’exécution

Sentence Transformers, les modèles locaux et PostgreSQL/pgvector ne sont pas installés dans cette validation. Les adaptateurs et le SQL de référence demandent un environnement verrouillé et une vérification réelle. Le code obligatoire ne requiert aucun de ces éléments.

Le tenant et la portée mémoire sont supposés fournis par un contexte autorisé; aucune authentification ni autorisation par document n’est implémentée. SQLite et le scan exact local ne constituent pas un index ANN distribué. L’expiration mémoire est logique et aucune purge automatique n’est annoncée.

## Reproduction

```bash
python3 scripts/validate_week09.py
python3 scripts/make_week09_reports.py
```
