# Objectifs pédagogiques — Sharing State

## Objectifs principaux

À la fin de cette journée, l'apprenant doit être capable de :

1. Expliquer pourquoi le partage d'état est un problème d'architecture et pas seulement une structure de données.
2. Distinguer état local, état partagé, conversation state et mémoire long terme.
3. Concevoir un store d'état partagé entre agents.
4. Versionner les écritures pour détecter les conflits.
5. Appliquer un modèle d'accès simple : privé, partagé, public.
6. Construire un handoff contextuel minimal.
7. Produire une trace exploitable des changements d'état.
8. Écrire des tests qui protègent les invariants du système.

## Compétences AI Engineering

Cette journée entraîne les compétences suivantes :

- design d'état applicatif ;
- coordination multi-agent ;
- réduction du contexte transmis au modèle ;
- maîtrise des effets de bord ;
- traçabilité ;
- isolation des responsabilités ;
- testabilité d'un composant agentique.

## Ce que l'apprenant doit savoir expliquer

L'apprenant doit pouvoir répondre clairement à ces questions :

- Pourquoi une mémoire globale partagée est dangereuse ?
- Quelle est la différence entre `state` et `memory` ?
- Pourquoi versionner les writes ?
- Quand faut-il utiliser un snapshot plutôt qu'un historique complet ?
- Que doit contenir un contexte de handoff ?
- Pourquoi les permissions d'état sont-elles importantes ?
- Comment détecter un conflit d'écriture ?
- Comment déboguer un workflow multi-agent grâce aux traces d'état ?

## Critères de réussite

La journée est réussie si l'apprenant peut :

- implémenter un store partagé simple ;
- refuser une écriture concurrente obsolète ;
- isoler les informations privées ;
- transmettre un contexte minimal entre agents ;
- écrire des tests unitaires pour les cas critiques ;
- expliquer les compromis entre simplicité, cohérence et observabilité.
