# Review formateur — Structured Outputs

## Objectif de la journée

La journée doit faire comprendre que les Structured Outputs ne sont pas une option cosmétique.

Ils sont une brique d’intégration backend.

Le message principal à faire passer :

```text
Un agent professionnel ne retourne pas seulement du texte.
Il retourne des contrats validables.
```

## Points à vérifier chez les apprenants

### Compréhension conceptuelle

L’apprenant doit pouvoir expliquer :

- pourquoi le texte libre est fragile ;
- pourquoi JSON valide ne signifie pas contrat valide ;
- la différence entre Function Calling et Structured Outputs ;
- le rôle d’un schéma ;
- pourquoi la validation côté application reste nécessaire.

### Compréhension architecture

L’apprenant doit savoir placer les Structured Outputs dans la chaîne :

```text
Model adapter
→ parser
→ validator
→ domain mapper
→ business logic
```

### Compréhension code

L’apprenant doit pouvoir lire et modifier :

- `TRIAGE_OUTPUT_SCHEMA` ;
- `validate_schema` ;
- `parse_triage_output` ;
- `TriageDecision` ;
- les tests invalides.

## Erreurs fréquentes

### Erreur 1 — Faire confiance au modèle

Certains apprenants vont directement faire :

```python
data = json.loads(output)
return data
```

Il faut insister sur le fait que `json.loads` ne valide pas le contrat métier.

### Erreur 2 — Corriger silencieusement

Exemple :

```python
if priority == "urgent":
    priority = "critical"
```

Cette correction peut sembler utile, mais elle cache une erreur de schéma.

### Erreur 3 — Mélanger message utilisateur et données machine

Le JSON machine doit être séparé de la réponse naturelle.

### Erreur 4 — Oublier les tests négatifs

Les tests invalides sont aussi importants que le cas nominal.

## Questions à poser en revue

1. Que se passe-t-il si le modèle ajoute un champ `refund_amount` ?
2. Que se passe-t-il si `confidence` vaut `"high"` ?
3. Où faut-il journaliser une sortie invalide ?
4. Quel fallback utiliser sur un ticket critique ?
5. Comment versionner ce schéma dans une vraie API ?

## Critères de validation pédagogique

La journée est réussie si l’apprenant peut :

- écrire un schéma simple ;
- expliquer chaque contrainte ;
- rejeter une sortie invalide ;
- mapper une sortie validée vers un objet métier ;
- relier cette logique à une architecture agentique.

## Préparation du jour suivant

Faire le lien avec le Conversation State :

- un état conversationnel doit être structuré ;
- les champs manquants doivent être représentés explicitement ;
- les décisions précédentes doivent être persistables ;
- une boucle agentique fiable dépend d’un état fiable.
