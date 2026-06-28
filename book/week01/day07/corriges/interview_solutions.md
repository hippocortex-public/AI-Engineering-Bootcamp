# Corrigés — Interview

## 1. Pourquoi créer un client LLM interne ?

Pour isoler la dépendance externe, centraliser la configuration, uniformiser la gestion d’erreurs, faciliter les tests et éviter de disperser les appels API dans toute l’application.

Un client interne permet aussi de changer de modèle ou de fournisseur avec moins d’impact.

## 2. Différence entre client, transport et configuration

- Le client expose l’interface utilisée par l’application.
- Le transport sait envoyer une requête à une implémentation concrète : mock, API OpenAI, autre fournisseur.
- La configuration contient les paramètres : modèle, clé API, timeout, température, limites de tokens.

## 3. Importance du mode mock

Le mode mock permet de tester sans réseau, sans coût, sans latence et sans variabilité de modèle. Il rend les tests unitaires déterministes.

## 4. Risques d’un prompt codé en dur

Un prompt codé en dur devient difficile à auditer, tester, versionner et réutiliser. Il mélange logique métier et logique d’interaction avec le modèle.

## 5. Validation des sorties structurées

Un LLM peut produire une réponse syntaxiquement incorrecte ou incomplète. La validation protège l’application contre les champs manquants, les types incorrects et les formats non exploitables.

## 6. Configuration vs validation

Une erreur de configuration concerne l’environnement d’exécution : clé API absente, modèle vide, timeout invalide.

Une erreur de validation concerne le résultat retourné : JSON invalide, champ obligatoire absent, valeur incohérente.

## 7. Pourquoi éviter une chaîne brute ?

Une chaîne brute ne contient ni métadonnées, ni modèle utilisé, ni réponse brute, ni informations de diagnostic. Une réponse typée facilite l’observabilité et l’évolution.

## 8. Paramètres configurables

- modèle ;
- température ;
- nombre maximal de tokens ;
- timeout ;
- clé API ;
- endpoint ;
- retries ;
- mode streaming ;
- format de sortie.

## 9. Préparation production

Il faut prévoir les timeouts, les erreurs, les logs, les métriques, les tests, la validation des sorties, la sécurité des secrets et la possibilité de changer de transport.

## 10. Quand l’abstraction est excessive ?

Pour un prototype très court, une exploration ponctuelle ou un notebook expérimental. Elle devient utile dès qu’un code est partagé, testé ou intégré dans une application.

## Questions pratiques

### Signature `generate_text`

```python
def generate_text(self, prompt: str, user_input: str | None = None) -> LLMResponse:
    ...
```

### Signature `generate_json`

```python
def generate_json(
    self,
    prompt: str,
    required_fields: list[str],
    user_input: str | None = None
) -> dict:
    ...
```

### Structure de réponse

```python
@dataclass
class LLMResponse:
    text: str
    model: str
    raw: dict[str, Any]
```

### Test sans réseau

```python
def test_generate_text_with_mock_transport():
    client = LLMClient(LLMConfig(model="mock-model"), MockTransport())
    response = client.generate_text("Bonjour")
    assert response.model == "mock-model"
```

### Remplacer le transport

Le client reçoit un transport injecté au constructeur. Pour passer du mock au réel, on garde la même classe `LLMClient` et on remplace uniquement :

```python
transport=MockTransport()
```

par :

```python
transport=OpenAIResponsesTransport()
```
