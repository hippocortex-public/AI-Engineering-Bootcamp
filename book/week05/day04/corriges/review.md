# Revue enseignant — Semaine 5 Jour 4

## Résumé pédagogique

Cette journée installe PostgreSQL comme brique durable des systèmes IA en production. L’objectif n’est pas de transformer les apprenants en DBA, mais de leur donner les réflexes nécessaires pour concevoir une persistance fiable d’assistant IA.

## Points à vérifier

L’apprenant doit comprendre que :

- Redis n’est pas la source de vérité durable ;
- PostgreSQL conserve les traces nécessaires à l’audit ;
- une conversation n’est pas suffisante sans runs et tool calls ;
- `JSONB` est utile mais ne remplace pas le modèle relationnel ;
- les transactions protègent la cohérence d’un tour ;
- les index doivent être justifiés par des requêtes ;
- le repository pattern protège le code métier.

## Erreurs fréquentes

### 1. Tout mettre dans une table messages

Symptôme : une table contient le rôle, le contenu, le modèle, les outils, les erreurs et les évaluations.

Correction : séparer `messages`, `agent_runs`, `tool_calls` et `evaluations`.

### 2. Utiliser JSONB comme modèle principal

Symptôme : les filtres importants sont enfouis dans `metadata`.

Correction : colonnes dédiées pour `status`, `model`, `created_at`, `tenant_id`, `conversation_id`.

### 3. Oublier l’échec

Symptôme : seuls les runs réussis sont persistés.

Correction : enregistrer les runs `failed` avec `error_message`.

### 4. Tester contre PostgreSQL uniquement

Symptôme : les tests unitaires deviennent lents et fragiles.

Correction : définir un contrat de repository et tester la logique métier avec un adaptateur mémoire.

## Déroulé recommandé

1. Commencer par la différence Redis / PostgreSQL.
2. Demander aux apprenants de lister les données à auditer.
3. Faire dessiner le schéma relationnel.
4. Introduire les contraintes.
5. Ajouter les requêtes de production.
6. Déduire les index à partir des requêtes.
7. Implémenter le repository.
8. Conclure avec la transaction d’un tour conversationnel.

## Questions de relance

- Que perdez-vous si vous ne stockez pas les tool calls ?
- Quels champs doivent devenir des colonnes et pourquoi ?
- Que se passe-t-il si l’écriture du message assistant échoue ?
- Comment retrouver les incidents d’un modèle précis ?
- Quelles données supprimeriez-vous lors d’une demande de rétention ?

## Checklist de correction

- [ ] Les tables ont une responsabilité unique.
- [ ] Les relations sont protégées par clés étrangères.
- [ ] Les rôles et statuts sont contraints.
- [ ] Les métadonnées variables utilisent `JSONB`.
- [ ] Les requêtes fréquentes ont des index.
- [ ] Les runs échoués sont persistés.
- [ ] Le repository masque la base.
- [ ] Les tests n’exigent pas PostgreSQL.
- [ ] La réponse distingue Redis et PostgreSQL.

## Propositions d’amélioration

Ces propositions ne modifient pas la spécification du jour. Elles peuvent être ajoutées dans une version future du projet :

- ajouter un module Alembic complet ;
- ajouter Row Level Security pour isoler les tenants ;
- brancher les événements PostgreSQL sur un pipeline d’évaluation ;
- ajouter un export anonymisé pour analyse qualité ;
- connecter le lab au projet FastAPI du Jour 2.
