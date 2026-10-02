# Objectifs pédagogiques — Semaine 5 Jour 4

## Objectif général

Construire une couche PostgreSQL adaptée à une application IA de production : durable, transactionnelle, auditable et testable.

## Objectifs détaillés

À la fin de cette journée, l’apprenant saura :

1. distinguer les responsabilités de Redis et PostgreSQL dans une architecture IA ;
2. modéliser les entités persistantes d’un assistant IA ;
3. concevoir un schéma relationnel pour conversations, messages, exécutions et appels d’outils ;
4. utiliser `JSONB` pour stocker des métadonnées évolutives sans casser le modèle relationnel ;
5. définir des contraintes d’intégrité adaptées aux systèmes agentiques ;
6. écrire des requêtes utiles pour reconstruire l’historique d’une conversation ;
7. choisir des index cohérents avec les accès de production ;
8. encapsuler l’accès aux données derrière un repository testable ;
9. préparer une stratégie de migration et d’évolution de schéma ;
10. expliquer les compromis entre normalisation, performance, audit et simplicité.

## Pré-requis

L’apprenant doit connaître :

- les bases de Python ;
- les principes d’une API FastAPI ;
- la notion d’état applicatif ;
- les bases SQL : tables, clés primaires, clés étrangères, index ;
- le rôle de Redis vu au Jour 3.

## Compétences AI Engineering

Cette journée renforce des compétences centrales d’AI Engineering :

- conception d’une couche data fiable ;
- historisation des interactions LLM ;
- traçabilité des décisions agentiques ;
- séparation entre état volatil et état durable ;
- préparation des systèmes d’évaluation et d’observabilité ;
- design de code orienté contrat.

## Critères de réussite

La journée est réussie si l’apprenant peut produire :

- un schéma PostgreSQL cohérent ;
- une transaction de persistance complète pour un tour de conversation ;
- une justification des index ;
- une interface repository testable ;
- une requête de reconstruction de conversation ;
- une analyse des risques de données en production.
