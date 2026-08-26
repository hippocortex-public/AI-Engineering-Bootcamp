# Corrigé — Challenge

## Approche attendue

Le challenge ajoute une couche de gouvernance entre l’extraction mémoire et l’écriture en mémoire longue.

Architecture :

```text
message utilisateur
→ extraction candidate
→ MemoryPolicy.evaluate(candidate)
→ audit
→ écriture conditionnelle
```

## Exemple de modèle de décision

```python
@dataclass
class MemoryDecision:
    allowed: bool
    reason: str
    memory_type: str | None = None
```

## Exemple de politique

```python
class MemoryPolicy:
    FORBIDDEN_PATTERNS = [
        "mot de passe",
        "password",
        "token",
        "api key",
        "carte bancaire",
        "malade",
        "déprimé",
    ]

    STATE_ONLY_PATTERNS = [
        "pour ce ticket",
        "commande",
        "order_id",
        "produit concerné",
    ]

    def evaluate(self, text: str, key: str | None = None) -> MemoryDecision:
        normalized = text.lower()

        if any(pattern in normalized for pattern in self.FORBIDDEN_PATTERNS):
            return MemoryDecision(False, "forbidden_sensitive_content")

        if any(pattern in normalized for pattern in self.STATE_ONLY_PATTERNS):
            return MemoryDecision(False, "state_only_information")

        if "je préfère" in normalized or "tu peux m'appeler" in normalized:
            return MemoryDecision(True, "explicit_preference", "preference")

        return MemoryDecision(False, "not_stable_or_not_useful")
```

## Audit attendu

Chaque tentative de mémorisation doit laisser une trace.

Exemple :

```json
{
  "user_id": "user_123",
  "source_text": "Je préfère les exemples en Python",
  "decision": "allowed",
  "reason": "explicit_preference",
  "memory_key": "language",
  "timestamp": "2026-08-24T14:00:00"
}
```

## Tests attendus

### 1. Préférence stockée

```python
def test_explicit_preference_is_stored():
    agent = GovernedMemoryAgent()
    agent.receive("u1", "Je préfère les exemples en Python")
    assert agent.memory.get_profile("u1").preferences["language"] == "Python"
```

### 2. Secret refusé

```python
def test_secret_is_rejected():
    agent = GovernedMemoryAgent()
    agent.receive("u1", "Mon mot de passe est hunter2")
    assert "hunter2" not in str(agent.memory.get_profile("u1").to_dict())
```

### 3. State non promu

```python
def test_ticket_data_is_not_long_term_memory():
    agent = GovernedMemoryAgent()
    agent.receive("u1", "Pour ce ticket, le produit concerné est Billing API")
    assert "Billing API" not in agent.memory.get_profile("u1").facts
```

### 4. Audit présent

```python
def test_audit_contains_decision():
    agent = GovernedMemoryAgent()
    agent.receive("u1", "Je préfère les réponses courtes")
    assert agent.audit_log[-1]["reason"] == "explicit_preference"
```

### 5. Oubli complet

```python
def test_forget_user_removes_audit():
    agent = GovernedMemoryAgent()
    agent.receive("u1", "Je préfère Python")
    agent.forget_user("u1")
    assert agent.audit_for("u1") == []
```

## Points de vigilance

- Ne pas ajouter de dépendance externe.
- Ne pas masquer les décisions de refus.
- Ne pas stocker le texte source complet si ce texte contient un secret.
- Préférer des champs structurés à une liste libre.
- Ajouter l’expiration uniquement lorsque cela clarifie le cycle de vie.

## Propositions d’amélioration

Ces propositions ne modifient pas les spécifications du bootcamp.

- Ajouter une UI de consultation mémoire utilisateur.
- Ajouter une stratégie d’expiration automatique.
- Ajouter une validation JSON Schema pour les décisions mémoire.
- Ajouter une métrique de précision d’extraction mémoire.
