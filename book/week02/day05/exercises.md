# Exercices — Memory courte, longue et state

## Exercice 1 — Classer les informations

Classe chaque élément dans une des catégories suivantes :

- short-term memory ;
- conversation state ;
- long-term memory ;
- ne pas mémoriser.

Éléments :

1. “L’utilisateur vient de demander un remboursement.”
2. “Le champ `order_id` manque pour terminer la tâche.”
3. “L’utilisateur préfère les exemples en Python.”
4. “Le dernier appel outil a retourné une erreur 404.”
5. “L’utilisateur a partagé un numéro de carte bancaire.”
6. “L’utilisateur souhaite qu’on l’appelle Sam.”
7. “Le statut de la tâche est `waiting_for_user`.”
8. “L’utilisateur était frustré dans le message précédent.”

## Exercice 2 — Concevoir un profil mémoire

Propose une structure JSON pour représenter une mémoire longue utilisateur.

Contraintes :

- inclure un identifiant utilisateur ;
- inclure un nom d’affichage optionnel ;
- inclure des préférences ;
- inclure des faits explicitement déclarés ;
- inclure une date de mise à jour ;
- ne pas inclure l’historique complet.

## Exercice 3 — Définir une politique de promotion

Écris une règle de promotion vers la mémoire longue pour chacune des phrases suivantes :

1. “Je préfère les réponses courtes.”
2. “Aujourd’hui je suis très fatigué.”
3. “Je travaille principalement avec FastAPI.”
4. “Mon mot de passe est hunter2.”
5. “Pour ce ticket, le produit concerné est Billing API.”
6. “Tu peux m’appeler Nadia.”

Pour chaque phrase, réponds :

- stocker ou ne pas stocker ;
- couche mémoire cible ;
- justification.

## Exercice 4 — Lire le code du lab

Dans `labs/memory_agent.py`, identifie :

1. où la mémoire courte est limitée ;
2. où le state est mis à jour ;
3. où la mémoire longue est isolée par utilisateur ;
4. où l’oubli utilisateur est implémenté ;
5. pourquoi les tests n’appellent pas de modèle externe.

## Exercice 5 — Étendre le test d’isolation

Ajoute un test qui vérifie que :

- l’utilisateur A indique préférer Python ;
- l’utilisateur B indique préférer TypeScript ;
- chaque utilisateur reçoit ensuite une réponse adaptée à sa préférence ;
- aucune préférence ne traverse la frontière utilisateur.

## Exercice 6 — Construire un contexte minimal

À partir des données suivantes, écris le contexte qui devrait être envoyé au modèle.

Profil :

```json
{
  "display_name": "Nadia",
  "preferences": {
    "language": "Python",
    "answer_style": "concise"
  }
}
```

State :

```json
{
  "intent": "create_support_ticket",
  "slots": {
    "product": "Billing API"
  },
  "missing_slots": ["description"],
  "status": "collecting"
}
```

Historique récent :

```text
user: L'API répond 500 depuis ce matin.
assistant: Quel produit est concerné ?
user: Billing API.
```

Objectif : produire un contexte utile sans inclure d’information inutile.

## Exercice 7 — Identifier les anti-patterns

Pour chaque pratique, explique le problème :

1. Stocker tous les messages dans une table `user_memory`.
2. Utiliser une mémoire globale partagée entre tous les utilisateurs.
3. Laisser le modèle décider seul de ce qui est persistant.
4. Ne pas fournir de méthode de suppression.
5. Réinjecter toute la mémoire longue dans chaque prompt.

## Exercice 8 — Mini-design

Conçois en 10 à 15 lignes une architecture mémoire pour un assistant de documentation technique.

L’assistant doit se souvenir :

- de la stack préférée ;
- du niveau d’expertise ;
- du format de réponse préféré.

Il ne doit pas mémoriser :

- les secrets ;
- les erreurs temporaires ;
- les données sensibles ;
- l’historique complet.
