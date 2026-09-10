# Corrigé — Challenge

## Approche recommandée

Ajouter une route admin dans le routeur `/v1`.

Pseudo-code :

```python
@router.post("/admin/sessions/{session_id}/forget")
def forget_session(
    session_id: str,
    x_human_approval: str | None = Header(default=None, alias="X-Human-Approval"),
):
    if x_human_approval != "approved":
        raise HTTPException(status_code=403, detail="human approval required")

    if session_id not in service.sessions:
        raise HTTPException(status_code=404, detail="session not found")

    del service.sessions[session_id]
    audit_log.append({
        "event": "session_forgotten",
        "session_id": session_id,
    })
    return {
        "status": "forgotten",
        "session_id": session_id,
    }
```

## Tests attendus

1. Créer une session avec `/v1/chat`.
2. Appeler `forget` sans `X-Human-Approval` : attendre `403`.
3. Appeler `forget` avec `X-Human-Approval: approved` : attendre `200`.
4. Relire la session : attendre `404`.
5. Vérifier que `/openapi.json` expose la route.

## Point d'architecture

L'oubli utilisateur est une action sensible.  
Elle doit être protégée par :

- authentification ;
- approbation humaine ou workflow équivalent ;
- audit log ;
- résultat structuré ;
- tests de non-régression.
