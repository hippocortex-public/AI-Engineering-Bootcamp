# Corrigés — Défis Day 2

## Défi débutant

Réponse attendue :

Le one-hot encoding identifie un mot mais ne dit rien sur son sens. Un embedding apprend une représentation dense dans laquelle des mots utilisés dans des contextes similaires deviennent proches. C'est cette proximité qui permet la recherche sémantique.

## Défi intermédiaire

| Approche | Avantage | Limite |
|---|---|---|
| One-hot | Simple, déterministe | Très grand, aucune sémantique |
| Word2Vec | Capture des similarités de mots | Peu adapté aux phrases complexes |
| Sentence embedding | Représente le sens global | Dépend fortement du modèle choisi |

## Défi AI Engineering

Architecture possible :

```text
Utilisateur -> API Search -> Embedding Model -> Vector DB -> Résultats -> LLM optionnel
```

Points importants :

- indexation offline des documents ;
- embedding des requêtes à la volée ;
- récupération top-k ;
- éventuellement reranking ;
- journalisation des requêtes pour améliorer la qualité.

## Défi architecte

La recherche vectorielle ne remplace pas toujours Elasticsearch.

Une bonne décision peut être :

- conserver Elasticsearch pour les filtres, exact match, facettes ;
- ajouter la recherche vectorielle pour la similarité sémantique ;
- combiner les deux dans une recherche hybride.

Décision recommandée : approche hybride plutôt que remplacement brutal.
