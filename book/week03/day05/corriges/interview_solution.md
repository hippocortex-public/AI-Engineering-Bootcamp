# Corrigé — Questions d'entretien — Sharing State

## Question 1

Le `conversation state` représente l'état courant d'une interaction : intention, slots, dernier contexte utile.

Le `shared state` représente l'état partagé d'un workflow multi-agent : faits, décisions, résultats intermédiaires, plan.

La `long-term memory` représente des informations durables qui peuvent survivre à une conversation ou à un workflow : préférences utilisateur, souvenirs synthétiques, profil.

## Question 2

Une mémoire globale partagée est dangereuse car elle mélange :

- données temporaires ;
- données durables ;
- brouillons privés ;
- décisions validées ;
- secrets ;
- historique brut.

Elle augmente les risques de fuite, de conflit et d'incohérence.

## Question 3

Le versioning sert à détecter les écritures obsolètes.

Un agent ne doit pas écraser une donnée qu'il a lue dans une version ancienne.

## Question 4

Le compare-and-set consiste à écrire une valeur uniquement si la version actuelle correspond à la version attendue.

Exemple :

```text
write key=plan.next_step expected_version=2
```

Si la version actuelle n'est pas `2`, l'écriture est refusée.

## Question 5

Un handoff doit contenir :

- l'objectif ;
- les faits validés ;
- les contraintes ;
- les clés nécessaires ;
- les incertitudes utiles ;
- le statut actuel.

## Question 6

Un handoff ne doit pas contenir :

- toutes les traces ;
- l'intégralité de l'historique ;
- les brouillons privés ;
- les secrets ;
- les données non nécessaires ;
- les raisonnements internes.

## Question 7

On évite la lecture d'une donnée privée avec une vérification systématique des permissions à chaque lecture ou snapshot.

La règle minimale :

```text
private => owner only
shared/public => visible selon politique du workflow
```

## Question 8

Journaliser les changements d'état permet :

- d'auditer le workflow ;
- de comprendre les bugs ;
- de reconstruire la chronologie ;
- d'analyser les conflits ;
- d'alimenter l'observabilité.

## Question 9

On expose une partie du shared state comme ressource MCP quand un agent externe ou un client MCP doit lire un contexte stable et autorisé.

Il faut éviter d'exposer les données privées, les secrets et les brouillons.

## Question 10

Je testerais :

- les lectures autorisées ;
- les lectures refusées ;
- les écritures versionnées ;
- les conflits ;
- les patches atomiques ;
- le handoff minimal ;
- le journal d'événements ;
- la sérialisation JSON.

## Question 11

Deux agents qui modifient le même plan en parallèle peuvent :

- écraser une modification récente ;
- produire deux versions contradictoires ;
- générer un handoff incohérent ;
- masquer un conflit métier.

Le versioning et le compare-and-set permettent de détecter ce cas.

## Question 12

Pour passer en production, je remplacerais le store en mémoire par :

- PostgreSQL ou Redis selon les besoins ;
- transactions ;
- verrous optimistes ;
- logs persistants ;
- chiffrement des champs sensibles ;
- expiration des données temporaires ;
- métriques et traces ;
- contrôle d'accès plus fin.
