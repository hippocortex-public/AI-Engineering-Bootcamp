# Corrigés — Questions d'entretien Day 2

## 1. Qu'est-ce qu'un embedding ?

Un embedding est une représentation vectorielle dense d'un objet : mot, phrase, document, image ou utilisateur. Pour le langage, il permet de représenter des similarités sémantiques dans un espace numérique.

## 2. Pourquoi le one-hot encoding est-il limité ?

Il crée des vecteurs très grands, très creux, et ne capture aucune proximité entre les mots.

## 3. Qu'est-ce que Word2Vec ?

Word2Vec est une famille de modèles qui apprend des représentations vectorielles de mots à partir de leurs contextes d'apparition.

## 4. CBOW vs Skip-gram

CBOW prédit le mot central à partir du contexte. Skip-gram prédit le contexte à partir du mot central.

## 5. Pourquoi les embeddings permettent-ils la recherche sémantique ?

Parce qu'ils rapprochent des textes similaires dans un espace vectoriel, même si les mots exacts ne correspondent pas.

## 6. Embedding de mot vs phrase

Un embedding de mot représente un token ou un mot. Un embedding de phrase représente une unité de sens plus large.

## 7. Pourquoi les RNN ?

Ils ont été conçus pour traiter des séquences en maintenant un état interne.

## 8. Limites des RNN

Ils ont du mal avec les longues dépendances et sont difficiles à paralléliser.

## 9. Pourquoi les LSTM ?

Les LSTM introduisent des mécanismes de portes pour mieux contrôler l'information retenue ou oubliée.

## 10. Cas d'usage recherche vectorielle

Documents internes, FAQ sémantique, recommandations, mémoire d'agent, clustering, détection de doublons.

## 11. Risques mémoire embeddings

Données sensibles, récupération non pertinente, stockage excessif, absence d'expiration, pollution de mémoire.

## 12. Évaluation embeddings

Tests de similarité, jeux de requêtes annotées, recall@k, precision@k, évaluation humaine.

## 13. Explication métier

Recherche mots-clés : "je trouve les mêmes mots". Recherche sémantique : "je trouve les documents qui parlent de la même idée".

## 14. Importance à l'ère LLM

Les embeddings sont essentiels pour connecter les LLM à des connaissances externes.

## 15. Compromis

Plus de qualité implique souvent plus de coût, plus de latence ou une infrastructure plus complexe.
