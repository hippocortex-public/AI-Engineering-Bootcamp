# Exercices — Semaine 5 Jour 4

## Exercice 1 — Répartition Redis / PostgreSQL

Classez chaque donnée dans Redis, PostgreSQL ou les deux.

| Donnée | Redis | PostgreSQL | Justification attendue |
|---|---:|---:|---|
| Rate limit utilisateur |  |  |  |
| Message utilisateur |  |  |  |
| Réponse assistant finale |  |  |  |
| Résultat temporaire de streaming |  |  |  |
| Run agent échoué |  |  |  |
| Session courte d’interface |  |  |  |
| Evaluation de qualité |  |  |  |
| Cache d’un appel outil |  |  |  |

## Exercice 2 — Schéma relationnel

Proposez un schéma minimal pour stocker :

- conversations ;
- messages ;
- runs agent ;
- appels d’outils.

Contraintes :

- chaque message appartient à une conversation ;
- chaque run appartient à une conversation ;
- chaque appel d’outil appartient à un run ;
- les rôles de message doivent être contrôlés ;
- les statuts de run doivent être contrôlés ;
- les métadonnées doivent accepter des champs variables.

## Exercice 3 — Transaction de tour conversationnel

Décrivez une transaction qui persiste un tour complet :

1. message utilisateur ;
2. run agent ;
3. appel LLM ;
4. éventuels appels d’outils ;
5. message assistant ;
6. statut final du run.

Précisez ce qui doit se passer en cas d’erreur après l’appel LLM mais avant l’écriture du message assistant.

## Exercice 4 — Indexation

Pour chaque requête, proposez un index.

### Requête A

```sql
select *
from conversations
where tenant_id = $1 and user_id = $2
order by created_at desc
limit 20;
```

### Requête B

```sql
select *
from messages
where conversation_id = $1
order by created_at asc;
```

### Requête C

```sql
select *
from agent_runs
where status = 'failed'
order by started_at desc
limit 50;
```

### Requête D

```sql
select model, avg(latency_ms)
from agent_runs
where status = 'succeeded'
group by model;
```

## Exercice 5 — Repository testable

Écrivez une interface Python `ConversationStore` avec trois méthodes :

- créer une conversation ;
- ajouter un message ;
- lister les messages.

Puis expliquez pourquoi un adaptateur mémoire est utile dans les tests.

## Exercice 6 — JSONB ou colonne dédiée ?

Pour chaque champ, indiquez s’il doit plutôt être une colonne dédiée ou une clé JSONB.

| Champ | Colonne | JSONB | Justification |
|---|---:|---:|---|
| `conversation_id` |  |  |  |
| `role` du message |  |  |  |
| `temperature` du modèle |  |  |  |
| `request_id` externe |  |  |  |
| `created_at` |  |  |  |
| `safety_profile` |  |  |  |
| `status` du run |  |  |  |
| `tool_arguments` |  |  |  |
