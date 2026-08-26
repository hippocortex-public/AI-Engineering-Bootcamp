# Exercices — Intégration du mini-framework

## Exercice 1 — Identifier les responsabilités

Associez chaque responsabilité au bon composant :

1. Valider les arguments d'une fonction.
2. Stocker une préférence utilisateur.
3. Détecter une dépendance cyclique.
4. Enregistrer un appel d'outil.
5. Définir les outils autorisés pour un agent.

Composants disponibles :

- `AgentSpec`
- `ToolRegistry`
- `MemoryStore`
- `WorkflowRunner`
- `Tracer`

## Exercice 2 — Contrat d'agent

Écrivez un `AgentSpec` pour un agent nommé `billing_agent`.

Contraintes :

- il doit traiter les demandes de facturation ;
- il peut appeler `classify_ticket`, `search_kb` et `draft_answer` ;
- il ne peut pas appeler directement `issue_refund`.

## Exercice 3 — Outil sensible

Expliquez pourquoi l'outil `issue_refund` doit être marqué comme sensible.

Proposez deux conditions minimales avant son exécution.

## Exercice 4 — Workflow

Soit le workflow suivant :

```text
classify → search_policy → draft_answer
```

Ajoutez une étape `risk_review` entre `search_policy` et `draft_answer`.

Décrivez les dépendances attendues.

## Exercice 5 — Trace minimale

Listez les événements qui devraient apparaître dans la trace pour une exécution réussie.

## Exercice 6 — Cas d'erreur

Pour chacun des cas suivants, indiquez le statut attendu :

1. outil inconnu ;
2. agent inconnu ;
3. outil sensible sans approbation ;
4. dépendance cyclique ;
5. exécution complète.

## Exercice 7 — Extension

Proposez une extension du framework pour préparer la semaine 5, sans modifier l'architecture existante.
