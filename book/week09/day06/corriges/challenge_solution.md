# Solution du challenge

remember(doc_id=kafka-replay) enregistre la version 1. Après ingest de la version 2, la jointure de recall ne correspond plus. Pour une note de style distincte, forget retire seulement la clé complète visée. Les autres sessions ne sont pas touchées et ne peuvent pas voir la note initiale.

## Vérification exécutable

Exécuter après les cellules du lab élève.

```python
from examples.week09.demo import documents
store = populated()
try:
    store.remember("team-a", "alice", "s1", "derived", "Synthèse de test", ttl=60, now=1000, doc_id="kafka-replay")
    assert store.recall("team-a", "alice", "s1", now=1001)
    original = documents()[0]
    store.ingest({**original, "version": 2, "text": "Nouvelle politique de paiement Kafka."})
    assert store.recall("team-a", "alice", "s1", now=1001) == []
    store.remember("team-a", "alice", "s1", "style", "Court", ttl=60, now=1000)
    store.forget("team-a", "alice", "s1", "style")
    assert store.recall("team-a", "alice", "s1", now=1001) == []
finally:
    store.close()
```
