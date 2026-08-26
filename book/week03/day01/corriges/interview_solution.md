# Corrigé — Questions d’entretien

## 1

Parce qu’une architecture multi-agents ajoute coût, latence, complexité, risques de boucle et difficulté de debug. Elle doit être justifiée par une séparation réelle des responsabilités.

## 2

Manager-worker : le manager garde le contrôle et agrège les résultats.  
Handoff : le contrôle est transféré à un spécialiste qui devient responsable de la suite.

## 3

Un reviewer est utile pour vérifier conformité, sécurité, format, complétude et ton. Il valide ou rejette, mais ne remplace pas le spécialiste métier.

## 4

Un état partagé trop large peut exposer des données sensibles, ajouter du bruit contextuel, créer des influences non souhaitées et compliquer l’audit.

## 5

Avec une limite d’itérations, des statuts terminaux, des règles de handoff explicites, un historique des agents appelés et un fallback vers humain ou clarification.

## 6

Tracer : session, étape, agent, action, entrée résumée, sortie structurée, décision, statut et erreur éventuelle.

## 7

Appel comme outil si le manager garde la réponse finale. Handoff si le spécialiste doit prendre le contrôle de la conversation.

## 8

Les sorties structurées rendent l’intégration testable, validable et observable.

## 9

Un router mal conçu produit mauvais handoffs, clarifications manquées, coûts inutiles et mauvaise expérience utilisateur.

## 10

Avec des agents mockés, règles déterministes, tests unitaires, contrats JSON, scénarios d’erreur et snapshots de traces.
