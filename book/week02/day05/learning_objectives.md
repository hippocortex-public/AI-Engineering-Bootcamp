# Objectifs pédagogiques — Semaine 2 Jour 5

## Objectifs principaux

À la fin de cette journée, l’apprenant doit être capable de construire une stratégie mémoire minimale mais professionnelle pour un agent IA.

## Compétences visées

### 1. Distinguer les couches mémoire

L’apprenant doit savoir expliquer :

- la différence entre historique récent et mémoire persistante ;
- la différence entre conversation state et long-term memory ;
- pourquoi une mémoire longue doit être sélective ;
- pourquoi la mémoire brute non gouvernée devient rapidement dangereuse.

### 2. Concevoir une mémoire courte

L’apprenant doit savoir :

- garder les derniers tours utiles ;
- limiter la taille de l’historique ;
- produire un résumé court ;
- choisir ce qui doit être injecté dans le prochain prompt.

### 3. Concevoir un état courant

L’apprenant doit savoir maintenir :

- une intention active ;
- des slots métier ;
- des champs manquants ;
- un statut de progression ;
- une trace des actions déjà effectuées.

### 4. Concevoir une mémoire longue

L’apprenant doit savoir :

- extraire des préférences explicites ;
- éviter les inférences fragiles ;
- stocker par utilisateur ;
- supprimer une mémoire utilisateur ;
- sérialiser une mémoire applicative.

### 5. Tester une mémoire d’agent

L’apprenant doit écrire des tests pour vérifier :

- l’isolation entre utilisateurs ;
- la rétention limitée de l’historique court ;
- la promotion sélective vers la mémoire longue ;
- l’absence de personnalisation inventée ;
- l’oubli contrôlé.

## Pré-requis

L’apprenant doit maîtriser :

- la boucle agentique ;
- les appels d’outils ;
- les sorties structurées ;
- la notion de conversation state ;
- les bases de Python : dataclasses, dictionnaires, tests simples.

## Livrable pratique attendu

Un mini-agent Python capable de :

- recevoir des messages multi-tours ;
- maintenir une mémoire courte ;
- maintenir un état de tâche ;
- extraire quelques préférences utilisateur ;
- personnaliser une réponse à partir d’une mémoire existante ;
- oublier un utilisateur ;
- passer une suite de tests automatisés.

## Critères d’évaluation

Un rendu est considéré correct si :

- le code est exécutable localement ;
- les tests passent sans dépendance externe ;
- les structures de données sont explicites ;
- les données persistantes sont isolées par utilisateur ;
- la mémoire longue ne contient pas de contenu arbitraire ;
- les décisions de stockage sont justifiables.

## Erreurs fréquentes à éviter

- Stocker tout l’historique en mémoire longue.
- Confondre résumé court et mémoire persistante.
- Réutiliser la mémoire d’un utilisateur pour un autre.
- Considérer les préférences comme éternellement vraies.
- Persister des données sensibles sans consentement ni politique d’oubli.
- Laisser le modèle décider seul de ce qui doit être mémorisé.
