# Corrigé — Challenge — Jour 6

## Solution attendue

Une solution correcte doit contenir :

- un état explicite ;
- un extracteur d'identifiant de commande ;
- un outil `lookup_order`;
- un outil `draft_support_reply`;
- une boucle bornée ;
- un journal d'exécution ;
- une condition d'arrêt ;
- un statut `completed` ou `waiting_for_user`.

## Exemple de déroulement nominal

Entrée :

```text
Bonjour, ma commande A-100 est en retard. Pouvez-vous m'aider ?
```

État initial :

```json
{
  "goal": "Résoudre une demande support",
  "order_id": "A-100",
  "order_status": null,
  "eta": null,
  "final_answer": null,
  "status": "running"
}
```

Itération 1 :

```json
{
  "action": "lookup_order",
  "arguments": {"order_id": "A-100"},
  "observation": {"status": "delayed", "eta": "2026-09-02"}
}
```

Itération 2 :

```json
{
  "action": "draft_support_reply",
  "arguments": {
    "order_id": "A-100",
    "status": "delayed",
    "eta": "2026-09-02"
  }
}
```

État final :

```json
{
  "status": "completed",
  "final_answer": "Bonjour, votre commande A-100 est actuellement retardée et sa livraison est estimée au 2026-09-02."
}
```

## Variante avec clarification

Entrée :

```text
Bonjour, ma commande est en retard.
```

L'agent doit produire :

```json
{
  "status": "waiting_for_user",
  "final_answer": "Pouvez-vous me transmettre votre identifiant de commande ?"
}
```

## Points de vigilance

Une solution incorrecte :

- invente un identifiant de commande ;
- appelle `lookup_order` sans argument ;
- ignore les erreurs d'outil ;
- ne journalise rien ;
- ne possède pas de limite d'itérations ;
- confond mémoire longue durée et state courant.
