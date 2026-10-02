# Challenge — Couche PostgreSQL pour assistant IA

## Contexte

Vous travaillez sur une plateforme d’assistants IA utilisée par plusieurs clients B2B. L’équipe dispose déjà d’une API FastAPI et d’un cache Redis. Elle veut maintenant ajouter une persistance durable avec PostgreSQL.

## Mission

Concevoir et implémenter une première version de la couche de persistance.

La solution doit stocker :

- les conversations ;
- les messages ;
- les runs agent ;
- les appels d’outils ;
- les évaluations simples.

## Contraintes

La solution doit :

1. utiliser PostgreSQL comme source durable ;
2. conserver Redis pour les usages volatils ;
3. isoler les conversations par `tenant_id` ;
4. permettre la reconstruction complète d’une conversation ;
5. permettre l’analyse des runs échoués ;
6. conserver les métadonnées variables en `JSONB` ;
7. éviter de disperser le SQL dans toute l’application ;
8. être testable sans base PostgreSQL réelle.

## Livrables attendus

Vous devez produire :

1. un schéma SQL ;
2. une proposition d’index ;
3. une interface Python de repository ;
4. un adaptateur mémoire de test ;
5. une stratégie transactionnelle ;
6. une liste d’anti-patterns à éviter ;
7. un plan de migration depuis une table `messages` unique.

## Critères d’acceptation

Le challenge est réussi si :

- chaque table a une responsabilité claire ;
- les relations sont protégées par des clés étrangères ;
- les rôles et statuts sont contraints ;
- les requêtes principales sont indexées ;
- le repository masque les détails de stockage ;
- les tests peuvent vérifier le comportement métier ;
- la réponse distingue clairement Redis et PostgreSQL.

## Bonus

Ajouter une table `evaluation_runs` pour regrouper plusieurs métriques d’évaluation par version de prompt, environnement ou modèle.
