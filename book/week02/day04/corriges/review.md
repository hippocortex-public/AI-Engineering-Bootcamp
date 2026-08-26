# Review formateur — Conversation State

## Objectif de la journée

La journée doit faire comprendre que le Conversation State est une brique backend, pas un détail de prompt.

Le message principal à faire passer :

```text
Un agent multi-tours fiable ne se souvient pas seulement grâce au modèle.
Il maintient un état applicatif explicite.
```

## Points à vérifier chez les apprenants

### Compréhension conceptuelle

L’apprenant doit pouvoir expliquer :

- pourquoi un agent stateless échoue en multi-tours ;
- la différence entre historique, state et memory ;
- ce qu’est un slot métier ;
- pourquoi les champs manquants doivent être explicites ;
- pourquoi la session doit être isolée.

### Compréhension architecture

L’apprenant doit savoir placer le Conversation State dans la chaîne :

```text
User message
→ Model or extractor
→ State updater
→ State validator
→ Action policy
→ Assistant response
→ State persistence
```

### Compréhension code

L’apprenant doit pouvoir lire et modifier :

- `ConversationState` ;
- `REQUIRED_FIELDS` ;
- `extract_slots` ;
- `missing_required_fields` ;
- `handle_user_message` ;
- `serialize_state` ;
- `restore_state`.

## Erreurs fréquentes

### Erreur 1 — Confondre historique et state

L’historique est utile, mais le backend a besoin d’une structure.

### Erreur 2 — Recalculer toute la conversation à chaque tour

C’est coûteux, fragile et peu testable.

### Erreur 3 — Stocker trop d’informations

Le state doit rester minimal.

Il ne doit pas devenir une base de données personnelle.

### Erreur 4 — Exécuter une action trop tôt

Un outil métier ne doit pas être appelé tant que les champs requis ne sont pas complets et valides.

### Erreur 5 — Oublier les tests multi-sessions

Les tests nominaux ne suffisent pas.

Il faut vérifier explicitement l’isolation.

## Questions à poser en revue

1. Pourquoi `ORD-1001` ne suffit-il pas sans contexte ?
2. Quels slots faut-il pour `refund` ?
3. Où stocker un résultat d’outil ?
4. Que faire si l’utilisateur corrige `order_id` ?
5. Pourquoi ne faut-il pas stocker un mot de passe dans le state ?
6. Comment tester l’absence de fuite entre deux sessions ?

## Critères de validation pédagogique

La journée est réussie si l’apprenant peut :

- créer un état conversationnel ;
- faire évoluer cet état sur plusieurs tours ;
- poser une question basée sur les champs manquants ;
- sérialiser et restaurer le state ;
- expliquer la frontière avec la memory ;
- identifier les risques de sécurité.

## Préparation du jour suivant

Faire le lien avec **Memory** :

- le state est court terme ;
- la memory peut survivre à plusieurs conversations ;
- toute information durable doit être choisie, justifiée et gouvernée ;
- la mémoire ne doit pas être une copie infinie du chat.
