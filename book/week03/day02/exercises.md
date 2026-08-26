# Exercices — Coordination multi-agents

## Exercice 1 — Identifier les rôles

Pour chaque situation, indique quel rôle est principalement nécessaire :

1. Choisir entre un agent support et un agent billing.
2. Vérifier qu'une réponse finale ne promet pas une action interdite.
3. Transformer trois analyses locales en réponse utilisateur.
4. Décider qu'une tâche doit être traitée par deux agents en parallèle.
5. Transférer une conversation client vers un agent juridique.

Réponds avec l'un des rôles suivants :

- router ;
- manager ;
- specialist ;
- reviewer ;
- synthesizer ;
- handoff.

## Exercice 2 — Sélection d'agents

On dispose des agents suivants :

```text
support_agent: support client, réponse utilisateur
billing_agent: facturation, paiements, remboursements
engineering_agent: bugs, logs, API, incidents
security_agent: accès, permissions, données sensibles
reviewer_agent: cohérence, risque, conformité
```

Pour chaque demande, liste les agents utiles :

1. "Le client a été facturé deux fois et demande une réponse."
2. "Analyse cette erreur 500 sur l'API de paiement."
3. "Peux-tu expliquer pourquoi un utilisateur n'a plus accès à son compte ?"
4. "Prépare une réponse client sur un bug qui a exposé des données."
5. "Résume une note produit sans risque particulier."

## Exercice 3 — Contexte minimal

Voici une demande :

```text
Un client entreprise signale une facture de 1 200 € au lieu de 120 €.
Il est très mécontent. Il mentionne aussi qu'un développeur a vu une erreur API hier.
Il demande un remboursement immédiat et une explication technique.
```

Définis le contexte minimal à transmettre :

1. à `billing_agent` ;
2. à `engineering_agent` ;
3. à `support_agent` ;
4. à `reviewer_agent`.

## Exercice 4 — Détection de conflit

Deux agents produisent les observations suivantes :

```text
engineering_agent:
- status: resolved
- finding: "L'incident API est corrigé depuis 10h."

support_agent:
- status: unresolved
- finding: "Le client indique que le problème est encore présent à 11h."
```

1. Y a-t-il conflit ?
2. Quelle décision doit prendre le coordinateur ?
3. Quelle réponse finale ne doit surtout pas être produite ?

## Exercice 5 — Politique de revue

Propose une règle simple qui déclenche `reviewer_agent` dans les cas suivants :

- risque élevé ;
- désaccord entre agents ;
- action sensible ;
- manque d'information ;
- réponse externe à un client entreprise.

## Exercice 6 — Trace d'exécution

Écris une trace JSON minimale pour une coordination qui :

- reçoit une tâche `task-42` ;
- sélectionne `support_agent` et `billing_agent` ;
- détecte aucun conflit ;
- ne déclenche pas de revue ;
- produit une réponse finale.

## Exercice 7 — Amélioration du lab

Dans le fichier `labs/multi_agent_coordinator.py`, ajoute un nouvel agent `legal_agent`.

Il doit être sélectionné lorsqu'une tâche contient un domaine `legal`.

Ajoute un test qui vérifie que :

- `legal_agent` est sélectionné ;
- la trace contient son résultat ;
- une revue est déclenchée si le risque est `high`.
