# Exercices — Abstraction Agent

## Exercice 1 — Identifier les responsabilités

Classe les responsabilités suivantes dans la bonne catégorie :

1. Construire le prompt système.
2. Exécuter une requête HTTP vers le fournisseur LLM.
3. Valider que l’entrée utilisateur n’est pas vide.
4. Choisir le prochain nœud d’un workflow.
5. Retourner un `AgentResult`.
6. Persister une mémoire long terme.
7. Injecter un faux modèle pour les tests.
8. Appliquer une limite de longueur d’entrée.

Catégories :

- Agent
- ModelClient
- Runner / Workflow
- Memory Layer
- Test / Infrastructure

## Exercice 2 — Concevoir un contrat

Propose une structure `RunContext` minimale pour un agent support.

Contraintes :

- elle doit contenir le message utilisateur ;
- elle doit distinguer `user_id` et `session_id` ;
- elle doit permettre d’ajouter des métadonnées ;
- elle doit rester sérialisable en JSON.

## Exercice 3 — Standardiser une sortie

Transforme cette sortie naïve :

```python
"Votre ticket est prioritaire."
```

en sortie structurée adaptée à un framework.

La sortie doit contenir :

- nom de l’agent ;
- statut ;
- réponse texte ;
- usage minimal ;
- trace minimale.

## Exercice 4 — Repérer les anti-patterns

Analyse le code suivant :

```python
class SupportAgent:
    def answer(self, question):
        from openai import OpenAI
        client = OpenAI()
        response = client.responses.create(
            model="gpt-4.1",
            input=f"Réponds: {question}"
        )
        return response.output_text
```

Liste au moins quatre problèmes pour un framework professionnel.

## Exercice 5 — Modifier le lab

Dans `agent_abstraction.py`, ajoute un guardrail qui bloque les entrées contenant le terme `DROP TABLE`.

Critères :

- le blocage doit retourner un `AgentResult` avec statut `blocked` ;
- le modèle ne doit pas être appelé ;
- une trace doit expliquer la raison du blocage.

## Exercice 6 — Préparer l’extension tools

Sans implémenter le `Tool Registry`, propose la modification minimale de l’API `Agent` permettant plus tard d’ajouter des tools.

Ne modifie pas encore le comportement d’exécution.
