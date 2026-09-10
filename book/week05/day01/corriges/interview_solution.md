# Corrigé — Questions d'entretien

## 1

Un appel direct au modèle depuis une route HTTP mélange transport, logique métier, prompt, fournisseur, sécurité et observabilité. En production, il faut contrôler les entrées, versionner les prompts, tracer les appels, gérer les erreurs, limiter les coûts et protéger les outils.

## 2

L’`Application Service` porte le cas d’usage produit. L’`Agent Runtime` exécute l’agent : instructions, modèle, outils, sorties, garde-fous et limites d’exécution.

## 3

Un `Model Gateway` centralise timeouts, retries, fallback, logging, version de modèle, budget de coût et normalisation des erreurs.

## 4

Un `Tool Gateway` vérifie identité, permissions, schéma d’arguments, portée de l’action, sensibilité, validation humaine, idempotence et audit.

## 5

Le `conversation state` est temporaire et lié à une session. Le `memory store` est durable et lié aux préférences ou faits réutilisables. La `business database` contient les données métier officielles du produit.

## 6

Il faut tracer request id, user/session id pseudonymisé, prompt version, model version, tool calls, latence, coût estimé, tokens, erreurs, garde-fous, sortie validée et statut final.

## 7

On limite le coût avec budget par requête, budget par utilisateur, limite d’itérations, limitation des outils, cache, résumé de contexte, choix de modèle adapté et alertes.

## 8

Un rollback doit pouvoir revenir à une version précédente de prompts, schémas, outils, modèle, policy de mémoire et configuration runtime.

## 9

Prompts et schémas doivent être versionnés pour assurer reproductibilité, audit, comparaison d’évaluations, rollback et débogage.

## 10

Un AI Backend Engineer doit refuser la mise en production si les outils sensibles ne sont pas protégés, les logs exposent des données sensibles, les coûts ne sont pas bornés, les sorties ne sont pas validées, aucune évaluation minimale n’existe, le rollback est impossible ou l’observabilité est insuffisante.
