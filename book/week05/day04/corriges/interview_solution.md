# Corrigé — Questions d’entretien Semaine 5 Jour 4

## 1. Pourquoi PostgreSQL plutôt que Redis pour l’historique durable ?

PostgreSQL offre durabilité, contraintes, transactions, requêtes SQL et relations fortes. Redis est plus adapté aux données volatiles, aux compteurs, au cache et aux sessions courtes.

## 2. Quelles données conserver pour l’audit ?

Il faut conserver les messages, les runs agent, les appels d’outils, les versions de prompt, le modèle utilisé, les paramètres importants, les erreurs, les timestamps et les évaluations.

## 3. Pourquoi ne pas tout stocker en JSONB ?

Parce que cela réduit la qualité des contraintes, rend les requêtes plus difficiles, complique les migrations et masque les relations importantes. `JSONB` doit compléter le modèle relationnel, pas le remplacer.

## 4. À quoi sert une transaction ?

Elle garantit qu’un tour conversationnel est persisté de manière cohérente. Sans transaction, on peut obtenir un message assistant sans run, un tool call sans contexte ou un statut final incohérent.

## 5. Différence entre message assistant et agent run

Le message assistant est le contenu visible produit pour l’utilisateur. L’agent run est l’exécution interne : modèle, statut, tokens, latence, outils, erreurs et version de prompt.

## 6. Pourquoi enregistrer les appels d’outils ?

Parce qu’ils expliquent les actions de l’agent. Sans eux, il devient difficile de comprendre pourquoi une réponse a été produite, de diagnostiquer une erreur ou de vérifier une action externe.

## 7. Index pour les messages d’une conversation

```sql
create index idx_messages_conversation_created
on messages (conversation_id, created_at asc);
```

## 8. Pourquoi un tenant_id ?

Il permet l’isolation logique des clients, la facturation, l’audit, l’export, la rétention et la suppression sélective.

## 9. Idempotence

L’idempotence garantit qu’un retry d’une même requête ne crée pas plusieurs fois la même donnée ou ne déclenche pas plusieurs fois la même action métier.

## 10. Repository pattern

Le repository pattern sépare le code métier du stockage. Il rend les tests plus simples et évite de disperser le SQL dans toute l’application.

## 11. Tables prioritaires pour un assistant IA B2B

Tables minimales :

- `conversations` ;
- `messages` ;
- `agent_runs` ;
- `tool_calls` ;
- `evaluations`.

Selon le contexte, on peut ajouter `users`, `tenants`, `prompt_versions` et `audit_events`.

## 12. Métadonnées variables d’un appel LLM

Les paramètres variables peuvent être stockés en `JSONB`, par exemple `metadata`. Les dimensions souvent filtrées, comme `model`, `status` ou `created_at`, doivent rester en colonnes dédiées.

## 13. Retrouver les 50 derniers runs échoués

```sql
select *
from agent_runs
where status = 'failed'
order by started_at desc
limit 50;
```

Index recommandé :

```sql
create index idx_agent_runs_status_started
on agent_runs (status, started_at desc);
```

## 14. Latence moyenne par modèle

```sql
select model, avg(latency_ms) as avg_latency_ms
from agent_runs
where status = 'succeeded'
group by model
order by avg_latency_ms desc;
```

## 15. Eviter les doublons lors d’un retry

Utiliser une clé d’idempotence unique, par exemple `idempotency_key`, et effectuer les insertions dans une transaction. En cas de conflit, retourner la ressource existante ou ignorer l’écriture dupliquée selon la logique métier.

## Cas pratique

### Risques

Une seule table `messages` ne permet pas de tracer :

- les versions de prompt ;
- les outils appelés ;
- les erreurs internes ;
- les latences ;
- les tokens ;
- les évaluations ;
- les statuts de run.

### Schéma minimal à ajouter

Ajouter :

- `conversations` pour structurer les fils ;
- `agent_runs` pour tracer les exécutions ;
- `tool_calls` pour expliquer les actions ;
- `evaluations` pour mesurer la qualité.

### Ordre de migration

1. Créer les nouvelles tables sans casser la table existante.
2. Remplir `conversations` à partir des regroupements existants.
3. Relier les messages à une conversation.
4. Ajouter progressivement les runs pour les nouveaux échanges.
5. Activer l’écriture duale temporaire si nécessaire.
6. Basculer la lecture vers le nouveau modèle.
7. Supprimer l’ancien chemin après validation.

### Bénéfices

Le nouveau modèle améliore le debug, l’audit, le monitoring, l’analyse de qualité et la maîtrise des coûts.
