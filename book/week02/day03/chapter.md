# Chapitre — Structured Outputs

## 1. Le problème des sorties non structurées

Un modèle de langage produit naturellement du texte.

Pour une démonstration, cela suffit :

```text
Le ticket semble urgent et concerne probablement un problème de facturation.
```

Pour un backend, cette phrase est insuffisante.

Une application doit souvent prendre des décisions concrètes :

- router un ticket vers une équipe ;
- déclencher une alerte ;
- créer une tâche ;
- renseigner une base de données ;
- calculer un SLA ;
- afficher une interface stable ;
- exécuter un workflow.

Dans ces cas, le texte libre devient un risque.

Le backend doit deviner :

- où se trouve la priorité ;
- quelle équipe est concernée ;
- si l’action est obligatoire ;
- quelle partie est un résumé ;
- si la valeur de confiance est exploitable ;
- si la réponse contient un format inattendu.

Un agent IA professionnel doit donc produire des données structurées, pas seulement du texte.

## 2. Définition

Un **Structured Output** est une réponse de modèle contrainte par un schéma.

Le schéma définit :

- la forme attendue ;
- les champs obligatoires ;
- les types ;
- les valeurs autorisées ;
- les objets imbriqués ;
- les contraintes de validation ;
- ce qui est interdit.

Exemple de sortie structurée :

```json
{
  "category": "billing",
  "priority": "high",
  "sentiment": "frustrated",
  "summary": "Le client signale une double facturation.",
  "action_required": true,
  "next_action": {
    "owner_team": "billing_ops",
    "rationale": "Le ticket mentionne un paiement prélevé deux fois."
  },
  "confidence": 0.91
}
```

Cette sortie est immédiatement exploitable par un programme.

## 3. Différence avec le Function Calling

Le jour précédent a introduit le Function Calling.

Le modèle produit alors une intention d’appel :

```json
{
  "name": "get_order_status",
  "arguments": {
    "order_id": "ORD-1001"
  }
}
```

L’application exécute ensuite l’outil.

Les Structured Outputs répondent à un besoin différent : contrôler la forme de la réponse finale ou intermédiaire.

Comparaison :

| Mécanisme | Question principale | Produit par le modèle | Utilisé pour |
|---|---|---|---|
| Texte libre | Que répondre ? | Phrase ou paragraphe | Chat simple |
| JSON libre | Peux-tu répondre en JSON ? | JSON non garanti | Prototype |
| JSON mode | Peux-tu produire du JSON valide ? | JSON syntaxiquement valide | Réponses simples |
| Function Calling | Quel outil appeler ? | Nom d’outil + arguments | Action externe |
| Structured Outputs | Quelle donnée conforme au schéma produire ? | Objet conforme au contrat | Intégration backend |

La distinction clé est la suivante :

> Le Function Calling structure une action. Les Structured Outputs structurent une donnée.

## 4. Pourquoi le JSON libre ne suffit pas

Demander à un modèle :

```text
Réponds uniquement en JSON.
```

ne suffit pas pour un système de production.

Le modèle peut produire :

```json
{
  "categorie": "facturation",
  "priority": "urgent",
  "confidence": "very high"
}
```

Ce JSON est syntaxiquement valide, mais il casse le contrat attendu :

- `categorie` est en français alors que le backend attend `category` ;
- `urgent` n’est peut-être pas une priorité autorisée ;
- `confidence` est une chaîne au lieu d’un nombre ;
- des champs obligatoires peuvent manquer.

Le problème n’est donc pas seulement la syntaxe JSON. Le problème est la conformité au contrat métier.

## 5. Le schéma comme contrat

Un schéma de sortie doit être traité comme une API interne.

Il doit répondre à ces questions :

- quels champs sont obligatoires ?
- quels types sont acceptés ?
- quelles valeurs sont autorisées ?
- quelles contraintes numériques existent ?
- les champs supplémentaires sont-ils interdits ?
- comment versionner le contrat ?
- qui consomme cette donnée ?

Exemple de contrat métier :

```json
{
  "type": "object",
  "required": [
    "category",
    "priority",
    "sentiment",
    "summary",
    "action_required",
    "next_action",
    "confidence"
  ],
  "additionalProperties": false,
  "properties": {
    "category": {
      "type": "string",
      "enum": ["billing", "technical", "account", "shipping", "other"]
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"]
    },
    "sentiment": {
      "type": "string",
      "enum": ["neutral", "frustrated", "angry", "satisfied"]
    },
    "summary": {
      "type": "string"
    },
    "action_required": {
      "type": "boolean"
    },
    "next_action": {
      "type": "object",
      "required": ["owner_team", "rationale"],
      "additionalProperties": false,
      "properties": {
        "owner_team": {
          "type": "string",
          "enum": ["support_l1", "billing_ops", "technical_ops", "account_ops"]
        },
        "rationale": {
          "type": "string"
        }
      }
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    }
  }
}
```

## 6. Architecture d’un pipeline Structured Output

Un pipeline robuste sépare plusieurs responsabilités :

```text
Prompt builder
→ Model adapter
→ JSON parser
→ Schema validator
→ Domain mapper
→ Business rule engine
```

Chaque composant a un rôle précis.

### Prompt builder

Il prépare la demande.

Il doit expliquer :

- la tâche ;
- les contraintes métier ;
- le schéma attendu ;
- les valeurs autorisées ;
- les exemples utiles ;
- les règles de refus ou d’incertitude.

### Model adapter

Il encapsule l’appel au modèle.

Dans un lab local, ce composant peut être remplacé par un faux modèle déterministe.

En production, il isole :

- le fournisseur LLM ;
- le modèle utilisé ;
- les paramètres ;
- les erreurs réseau ;
- les mécanismes de retry.

### JSON parser

Il convertit la chaîne produite en objet Python.

Il doit échouer proprement si la sortie n’est pas du JSON valide.

### Schema validator

Il vérifie la conformité au contrat.

Il doit détecter :

- champs manquants ;
- types incorrects ;
- valeurs non autorisées ;
- nombres hors bornes ;
- propriétés inattendues ;
- objets imbriqués invalides.

### Domain mapper

Il convertit le dictionnaire validé en objet métier.

Par exemple :

```python
TriageDecision(
    category="billing",
    priority="high",
    sentiment="frustrated",
    summary="Le client signale une double facturation.",
    action_required=True,
    owner_team="billing_ops",
    confidence=0.91,
)
```

### Business rule engine

Il applique les règles internes.

Exemple :

```text
Si priority = critical et confidence >= 0.85
→ créer une alerte immédiate
```

Le modèle ne doit pas être le seul responsable des règles critiques.

## 7. Les Structured Outputs dans une architecture agentique

Dans une architecture agentique, les Structured Outputs peuvent intervenir à plusieurs endroits :

1. **Classification de l’intention**
2. **Planification**
3. **Sélection d’outil**
4. **Extraction de paramètres**
5. **Résumé d’état**
6. **Décision de routage**
7. **Réponse finale typée**

Exemple :

```text
Utilisateur
→ Agent
→ Structured Output: intent = "support_triage"
→ Function Calling: retrieve_customer_profile(customer_id)
→ Structured Output: triage_decision
→ Réponse utilisateur
```

Les Structured Outputs ne remplacent pas les outils. Ils rendent les décisions de l’agent plus contrôlables.

## 8. Validation stricte et sécurité

Une sortie structurée ne doit pas être utilisée avant validation.

Règle fondamentale :

> Une donnée produite par un modèle est une entrée non fiable tant qu’elle n’a pas été validée.

Même si un fournisseur garantit une forte conformité au schéma, l’application doit garder une frontière de validation.

Pourquoi ?

- défense en profondeur ;
- portabilité entre modèles ;
- tests locaux ;
- robustesse face aux changements de modèle ;
- meilleure observabilité ;
- erreurs métier plus explicites.

## 9. Exemple de rupture

Ticket utilisateur :

```text
Je suis très énervé. Vous m’avez facturé deux fois ce mois-ci.
```

Sortie invalide :

```json
{
  "category": "billing",
  "priority": "urgent",
  "sentiment": "furious",
  "summary": "Double facturation.",
  "action_required": true,
  "next_action": {
    "owner_team": "finance"
  },
  "confidence": 1.2
}
```

Problèmes :

- `urgent` n’est pas une valeur autorisée ;
- `furious` n’est pas une valeur autorisée ;
- `owner_team` vaut `finance`, non prévu ;
- `rationale` manque ;
- `confidence` dépasse 1.

Un bon backend ne corrige pas silencieusement cette sortie. Il la rejette, la journalise et déclenche une stratégie de récupération.

## 10. Stratégies de récupération

Quand la validation échoue, plusieurs stratégies sont possibles :

### Réessayer avec le même schéma

Approprié si l’erreur est probablement ponctuelle.

```text
La sortie ne respecte pas le schéma. Regénère uniquement un JSON conforme.
```

### Réduire la tâche

Approprié si la sortie est trop complexe.

Exemple :

1. extraire uniquement la catégorie ;
2. extraire ensuite la priorité ;
3. produire enfin le résumé.

### Fallback déterministe

Approprié si la décision est critique.

Exemple :

```text
Si la priorité n’est pas validable, router vers support_l1.
```

### Escalade humaine

Approprié si le risque métier est élevé.

Exemple :

```text
Si le ticket contient une menace juridique ou un montant élevé, demander une revue humaine.
```

## 11. Anti-patterns

### Anti-pattern 1 — Parser du texte naturel

Mauvais :

```python
if "urgent" in model_response:
    priority = "high"
```

Ce code est fragile.

### Anti-pattern 2 — Faire confiance au modèle

Mauvais :

```python
decision = json.loads(model_response)
create_refund(decision["amount"])
```

Il manque validation, autorisation et règle métier.

### Anti-pattern 3 — Changer le schéma sans version

Mauvais :

```json
{
  "priority": "high"
}
```

puis plus tard :

```json
{
  "priority_level": "P1"
}
```

Si le consommateur n’est pas migré, l’intégration casse.

### Anti-pattern 4 — Mélanger réponse utilisateur et donnée machine

Mauvais :

```json
{
  "message": "Bonjour, nous allons vous aider.",
  "category": "billing",
  "priority": "high"
}
```

Ce format mélange deux responsabilités. Il vaut mieux séparer :

- la décision machine ;
- le message utilisateur.

## 12. Bonnes pratiques

### Définir des enums

Les enums réduisent l’ambiguïté.

```json
"priority": {
  "type": "string",
  "enum": ["low", "medium", "high", "critical"]
}
```

### Interdire les propriétés supplémentaires

Cela évite que le modèle invente des champs non consommés.

```json
"additionalProperties": false
```

### Garder les résumés courts

Un résumé doit être utile à l’interface ou à l’opérateur.

### Ajouter une confiance bornée

Un score de confiance n’est utile que s’il est borné.

```json
"confidence": {
  "type": "number",
  "minimum": 0,
  "maximum": 1
}
```

### Valider côté application

Le schéma côté modèle ne remplace pas le contrôle côté backend.

### Tester les cas invalides

Les tests doivent couvrir :

- JSON invalide ;
- champ manquant ;
- enum invalide ;
- type incorrect ;
- champ supplémentaire ;
- nombre hors bornes.

## 13. Lien avec le jour suivant

Le jour suivant porte sur le **Conversation State**.

Les Structured Outputs préparent ce sujet parce qu’un état de conversation doit être stocké sous forme fiable.

Exemple :

```json
{
  "current_intent": "refund_request",
  "missing_fields": ["order_id"],
  "last_confirmed_order_id": null,
  "should_ask_followup": true
}
```

Sans sortie structurée, l’état devient une collection de textes difficiles à maintenir.

## 14. Synthèse

Les Structured Outputs sont un outil central de l’AI Engineering.

Ils permettent de passer de :

```text
Le modèle a répondu quelque chose de plausible.
```

à :

```text
Le modèle a produit une donnée conforme, validée et exploitable.
```

Dans un système agentique, cette différence sépare une démonstration fragile d’un backend intégrable.
