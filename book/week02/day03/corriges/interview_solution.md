# Corrigé — Questions d’entretien Structured Outputs

## Question 1

Un JSON syntaxiquement valide peut être inutilisable s’il ne respecte pas le contrat métier.

Exemples :

- champ obligatoire absent ;
- mauvais nom de champ ;
- type incorrect ;
- valeur hors enum ;
- champ supplémentaire ;
- nombre hors bornes.

La validité JSON ne garantit que la structure syntaxique, pas la conformité métier.

## Question 2

Le Function Calling structure une action : le modèle choisit un outil et fournit des arguments.

Les Structured Outputs structurent une donnée : le modèle produit un objet conforme à un schéma, souvent utilisé comme décision, extraction ou état intermédiaire.

Formule courte :

```text
Function Calling = action à exécuter.
Structured Outputs = donnée à consommer.
```

## Question 3

Il faut valider côté application pour garder une frontière de sécurité.

Raisons :

- défense en profondeur ;
- robustesse face aux changements de modèle ;
- détection explicite des erreurs ;
- portabilité entre fournisseurs ;
- tests locaux ;
- protection des systèmes aval.

Un modèle est une source d’entrée, pas une autorité de confiance.

## Question 4

Les champs souvent contraints par enums sont :

- `intent` ;
- `category` ;
- `priority` ;
- `sentiment` ;
- `owner_team` ;
- `next_step` ;
- `tool_name` ;
- `status` ;
- `risk_level`.

Les enums réduisent l’ambiguïté et facilitent le routage.

## Question 5

Dans un système critique :

1. rejeter la sortie invalide ;
2. journaliser l’erreur ;
3. tenter une régénération contrôlée ;
4. appliquer un fallback déterministe ;
5. escalader vers un humain si nécessaire ;
6. ne jamais exécuter une action critique à partir d’une donnée non validée.

## Question 6

`additionalProperties: false` empêche le modèle d’ajouter des champs non prévus.

Cela évite :

- la dérive du contrat ;
- les données ignorées mais trompeuses ;
- les erreurs silencieuses ;
- les ambiguïtés entre versions ;
- l’exploitation de champs non validés.

## Question 7

Le Conversation State doit être fiable, stable et sérialisable.

Les Structured Outputs permettent de représenter l’état sous forme d’objet :

```json
{
  "intent": "refund",
  "missing_fields": ["order_id"],
  "should_ask_followup": true
}
```

Cela rend l’agent plus contrôlable qu’un historique interprété uniquement en texte libre.

## Question 8

Tests à écrire :

- JSON invalide ;
- champ obligatoire manquant ;
- enum invalide ;
- type incorrect ;
- confidence inférieure à 0 ;
- confidence supérieure à 1 ;
- propriété supplémentaire ;
- objet imbriqué incomplet ;
- cas valide complet ;
- mapping vers objet métier.
