# Références — J4

Sources primaires consultées le 20 octobre 2026. Les algorithmes et contrats du lab sont explicités dans le chapitre; le corpus est une création fictive du cours.

- [pgvector : documentation officielle](https://github.com/pgvector/pgvector) — stockage, distances, recherche exacte/ANN et filtres.
- [Sentence Transformers : retrieve and rerank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) — architecture de récupération en deux étapes.
- [SentenceTransformer : API](https://www.sbert.net/docs/package_reference/sentence_transformer/model.html) — encode_query, encode_document et modèles locaux.
- [CrossEncoder : API](https://www.sbert.net/docs/package_reference/cross_encoder/model.html) — scoring conjoint de paires.
- [Cormack, Clarke et Buettcher, SIGIR 2009 : Reciprocal Rank Fusion](https://research.google/pubs/reciprocal-rank-fusion-outperforms-condorcet-and-individual-rank-learning-methods/) — origine de la méthode de fusion des rangs.
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html) — persistance locale et transactions.

Lire en priorité les références du thème du jour. Les extensions évoluent; leur environnement réel doit être verrouillé et testé avant utilisation. Le paquet n’affirme pas avoir exécuté de modèle neuronal ou de serveur pgvector.
