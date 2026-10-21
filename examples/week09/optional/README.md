# Extensions optionnelles : embeddings neuronaux, reranker et pgvector

Ces éléments ne sont pas requis pour les labs. Ils n’ont pas été exécutés : ni sentence-transformers, ni les poids des modèles, ni PostgreSQL/pgvector ne sont présents dans l’environnement de validation. Les API ont été vérifiées dans la documentation officielle; l’intégration réelle doit être validée sur vos versions.

## Modèles locaux

Installer sentence-transformers dans un environnement séparé et retenir la version effectivement résolue dans un fichier de verrouillage de votre expérience. Préparer des modèles locaux compatibles avec la langue et la tâche, en vérifiant leurs licences et ressources nécessaires. Aucun modèle n’est téléchargé par le code : local_files_only est activé et trust_remote_code est désactivé.

Depuis la racine du dépôt :

```python
from examples.week09.optional.local_models import LocalSentenceEmbedding, LocalCrossEncoder
from examples.week09.knowledge import Store
from examples.week09.demo import documents

embedding = LocalSentenceEmbedding('/chemin/vers/modele-embedding-local')
store = Store('/tmp/s9-neural.sqlite', embedding=embedding)
try:
    for doc in documents():
        store.ingest(doc)
    query = 'Comment rejouer un paiement avec Kafka ?'
    candidates = store.search(query, 'team-a', top_k=12)
    reranker = LocalCrossEncoder('/chemin/vers/modele-cross-encoder-local')
    ranked = reranker.rerank(query, candidates)
    print([(c['doc_id'], c['score']) for c in ranked[:3]])
finally:
    store.close()
```

Utiliser un modèle de reranking à score scalaire par paire. Ses scores ne sont pas nécessairement des probabilités. Le constructeur calcule une empreinte des fichiers locaux; un changement de modèle nécessite une nouvelle base. Le modèle de query et celui de document doivent partager un espace compatible et les prompts prévus par l’encodeur. Une projection hashbow ne doit pas être mélangée aux vecteurs neuronaux.

## pgvector

`pgvector.sql` fournit un schéma et une requête paramétrée de référence, sans identifiants de connexion. Après création d’une base de lab, appliquer le schéma avec un rôle autorisé et charger les embeddings au moyen de votre client PostgreSQL. Commencer par la recherche exacte, puis mesurer le rappel et la latence d’un index ANN sur le même corpus.

Ce paquet ne livre pas d’adaptateur PostgreSQL testé. Le SQL n’installe ni serveur ni extension à votre place. La sélection d’une version de PostgreSQL/pgvector et le verrouillage des dépendances font partie de l’expérience optionnelle. Les accès et l’isolation restent à appliquer côté serveur; le tenant ne vient pas d’une déclaration client libre.
