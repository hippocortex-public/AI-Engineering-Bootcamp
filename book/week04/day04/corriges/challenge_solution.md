# Corrigé — Challenge

## Solution attendue

La solution fournie dans le lab implémente :

- `MemoryRecord`
- `MemoryQuery`
- `MemorySearchResult`
- `MemoryStore`
- `redact_pii`
- `promote_event`
- `snapshot`
- `from_snapshot`

## Points clés

### Isolation

Chaque record appartient à un namespace. `retrieve` et `forget_namespace` filtrent strictement sur ce namespace.

### Visibilité

Le champ `allowed_visibility` de `MemoryQuery` contrôle les records injectables.

### Expiration

Les records expirés sont exclus par défaut. Ils restent consultables uniquement si `include_expired=True`.

### Audit

Chaque `add`, `update`, `delete` et `forget` écrit un événement dans `audit_log`.

### Snapshot

`snapshot()` produit une structure JSON sérialisable. `from_snapshot()` restaure un store équivalent.

## Exemple

```python
store = MemoryStore()
store.add(
    namespace="user:42",
    owner_agent="planner",
    kind="preference",
    content="L'utilisateur préfère les étapes numérotées.",
    visibility="private",
    tags=["preference", "format"],
    importance=0.9,
)

results = store.retrieve(
    MemoryQuery(
        namespace="user:42",
        text="format étapes",
        allowed_visibility=("private", "shared"),
    )
)
```

## Vérification

Les tests du lab valident les critères d'acceptation du challenge.
