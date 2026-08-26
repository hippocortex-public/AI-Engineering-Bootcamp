# Chapitre — Agent Loop & planification

## 1. Pourquoi une boucle agentique ?

Un appel LLM classique suit souvent ce schéma :

```text
input utilisateur -> modèle -> réponse
```

Ce schéma fonctionne pour une réponse simple, mais il devient insuffisant quand la tâche demande :

- plusieurs étapes ;
- des outils ;
- une vérification intermédiaire ;
- une collecte d'information ;
- une mise à jour d'état ;
- une décision de continuation.

Un agent ajoute une boucle d'orchestration :

```text
objectif -> plan -> action -> observation -> état -> décision
```

Le modèle peut proposer des actions, mais l'application reste responsable de l'exécution, de la validation et de l'arrêt.

## 2. Anatomie d'une boucle agentique

Une boucle agentique minimale contient cinq composants.

### 2.1 Goal

Le `goal` est l'objectif demandé par l'utilisateur.

Exemple :

```text
Prépare un résumé de ticket support pour une commande retardée.
```

Le goal ne doit pas être modifié silencieusement. Il doit rester accessible dans l'état.

### 2.2 State

Le `state` contient ce que le système sait à un instant donné.

Exemple :

```json
{
  "goal": "Préparer un résumé de ticket support",
  "known_facts": {
    "order_id": "A-100",
    "status": "delayed"
  },
  "missing_facts": ["customer_name"],
  "iterations": 2
}
```

Le state n'est pas la mémoire longue durée. Il représente la situation courante de résolution.

### 2.3 Plan

Le plan est une liste d'étapes intentionnelles.

Exemple :

```json
[
  {"id": "step_1", "description": "Récupérer les informations de commande"},
  {"id": "step_2", "description": "Identifier la cause du retard"},
  {"id": "step_3", "description": "Rédiger une réponse synthétique"}
]
```

En production, ce plan peut venir d'un LLM via Structured Outputs. Dans le lab, il est simulé pour rester exécutable sans clé API.

### 2.4 Action

Une action est une opération décidée pour avancer dans le plan.

Elle peut être :

- un appel d'outil ;
- une question de clarification ;
- une transformation locale ;
- une réponse finale.

Exemple :

```json
{
  "tool_name": "lookup_order",
  "arguments": {"order_id": "A-100"}
}
```

### 2.5 Observation

L'observation est le résultat d'une action.

Exemple :

```json
{
  "tool_name": "lookup_order",
  "success": true,
  "data": {
    "status": "delayed",
    "eta": "2026-09-02"
  }
}
```

L'observation doit être séparée de l'action. Cela permet de tracer ce qui a été demandé et ce qui a été obtenu.

## 3. Cycle plan → act → observe → decide

La boucle minimale ressemble à ceci :

```python
state = initialize_state(goal)

while not state.done and state.iterations < max_iterations:
    action = policy.next_action(state)
    observation = tool_registry.execute(action)
    state = reducer.apply(state, action, observation)
    state.done = policy.should_finish(state)
```

Chaque étape doit être testable séparément.

## 4. Planification initiale

La planification initiale transforme un objectif vague en étapes exploitables.

Exemple :

Objectif :

```text
Aide-moi à traiter un ticket client sur une commande en retard.
```

Plan :

```text
1. Extraire l'identifiant de commande.
2. Consulter l'état de commande.
3. Préparer une réponse support.
4. Vérifier que la réponse mentionne le délai estimé.
```

La planification initiale ne doit pas exécuter les outils. Elle décrit seulement une stratégie.

## 5. Replanification

La replanification se produit quand une observation invalide le plan initial.

Exemples :

- l'identifiant de commande est absent ;
- l'outil retourne une erreur ;
- une donnée obligatoire manque ;
- le résultat contredit une hypothèse ;
- l'utilisateur ajoute une contrainte.

La replanification n'est pas un échec. C'est une propriété normale des agents.

## 6. Politique de décision

Une politique de décision répond à trois questions :

1. Quelle action exécuter maintenant ?
2. La tâche est-elle terminée ?
3. Faut-il demander une clarification ?

Exemple de logique :

```text
Si order_id est absent -> demander clarification.
Sinon si order_status est absent -> appeler lookup_order.
Sinon si final_answer est absent -> appeler draft_response.
Sinon -> terminer.
```

Cette logique peut être codée, générée par modèle, ou hybride.

## 7. Limites d'itérations

Un agent doit toujours avoir une limite d'itérations.

Sans limite, un agent peut :

- appeler le même outil plusieurs fois ;
- tourner en boucle sur une information manquante ;
- consommer des ressources inutilement ;
- produire des traces difficiles à analyser.

Exemple :

```python
max_iterations = 5
```

Si la limite est atteinte, l'agent doit retourner un état contrôlé :

```json
{
  "status": "max_iterations_reached",
  "final_answer": null
}
```

## 8. Observabilité

Chaque itération doit laisser une trace :

```json
{
  "iteration": 2,
  "action": "lookup_order",
  "observation": "status=delayed",
  "state_delta": ["order_status", "eta"]
}
```

Ces traces servent à :

- comprendre les décisions ;
- rejouer un scénario ;
- tester un bug ;
- auditer l'agent ;
- améliorer les prompts et les outils.

## 9. Erreurs fréquentes

### 9.1 Tout mettre dans le prompt

Un prompt ne remplace pas une architecture.

Erreur :

```text
Tu es un agent. Réfléchis étape par étape et utilise les outils si nécessaire.
```

Cette instruction est insuffisante si l'application ne contrôle pas :

- les outils disponibles ;
- les arguments ;
- les observations ;
- l'état ;
- l'arrêt.

### 9.2 Ne pas séparer action et observation

Mauvaise pratique :

```python
state["order"] = lookup_order(order_id)
```

Meilleure pratique :

```python
action = ToolAction("lookup_order", {"order_id": order_id})
observation = registry.execute(action)
state = reducer.apply(state, action, observation)
```

La séparation rend le système plus testable.

### 9.3 Pas de condition d'arrêt

Un agent doit savoir quand terminer.

Critères possibles :

- réponse finale disponible ;
- objectif atteint ;
- information bloquante manquante ;
- utilisateur doit répondre ;
- limite d'itérations atteinte ;
- erreur non récupérable.

## 10. Architecture recommandée

Une boucle agentique maintenable peut être découpée en quatre blocs :

```text
Planner
Policy
ToolRegistry
Reducer
```

- `Planner` crée ou met à jour le plan.
- `Policy` choisit la prochaine action.
- `ToolRegistry` exécute les outils autorisés.
- `Reducer` met à jour l'état à partir de l'observation.

Ce découpage est plus facile à tester qu'une fonction monolithique.

## 11. Exemple métier

Cas : assistant support e-commerce.

Objectif utilisateur :

```text
Réponds au client : ma commande A-100 est en retard.
```

Boucle :

1. extraire `order_id=A-100` ;
2. appeler `lookup_order`;
3. observer `status=delayed`, `eta=2026-09-02` ;
4. appeler `draft_support_reply`;
5. produire la réponse finale ;
6. terminer.

Ce type de scénario ressemble à un agent réel, mais reste suffisamment borné pour être testé.

## 12. Lien avec les jours précédents

- **J2 Function Calling** : les actions peuvent devenir des tool calls.
- **J3 Structured Outputs** : le plan et les actions peuvent être contraints par schéma.
- **J4 Conversation State** : l'état de résolution vit pendant la conversation.
- **J5 Memory** : certaines préférences persistantes peuvent influencer la politique.

## 13. Ce qu'il faut retenir

Une boucle agentique est un système d'orchestration.

Le modèle peut aider à planifier et décider, mais l'application doit contrôler :

- les outils ;
- les schémas ;
- les transitions d'état ;
- les erreurs ;
- les limites ;
- la traçabilité ;
- la condition finale.

Un bon agent est moins magique, mais beaucoup plus fiable.
