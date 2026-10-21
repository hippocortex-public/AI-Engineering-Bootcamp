# Solution du challenge

Utiliser une base temporaire fichier. Après ingest de la version 2, citation_valid sur l’ancien chunk retourne False. La réouverture retrouve la version 2. Après delete_document, la recherche et citation_valid ne doivent plus retourner la source supprimée. Garder les autres documents inchangés.

## Vérification exécutable

Exécuter après les cellules du lab élève.

```python
from examples.week09.demo import documents
store = Store()
try:
    original = documents()[0]
    store.ingest(original)
    hit = store.search("paiement Kafka", "team-a", top_k=1)[0]
    assert store.citation_valid(hit, "team-a")
    store.ingest({**original, "version": 2, "text": "Nouvelle procédure de paiement Kafka."})
    assert not store.citation_valid(hit, "team-a")
    store.delete_document("team-a", original["doc_id"])
    assert store.search("paiement Kafka", "team-a") == []
finally:
    store.close()
```
