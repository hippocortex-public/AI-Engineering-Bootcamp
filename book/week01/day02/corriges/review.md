# Review — Erreurs fréquentes Day 2

## Erreur 1 — Penser qu'un embedding comprend réellement le sens

Un embedding capture des régularités statistiques. Il ne comprend pas comme un humain.

## Erreur 2 — Confondre embedding et LLM

Un modèle d'embedding produit des vecteurs. Un LLM génère du texte.

## Erreur 3 — Croire que la recherche vectorielle remplace toujours la recherche classique

La recherche vectorielle est excellente pour la similarité sémantique. Elle est moins adaptée aux contraintes exactes, aux filtres complexes ou aux recherches booléennes.

## Erreur 4 — Stocker toute la mémoire d'un agent sous forme vectorielle

Une bonne mémoire combine souvent :

- base relationnelle ;
- cache ;
- résumé ;
- vector store ;
- règles de rétention.

## Erreur 5 — Ne pas évaluer les embeddings

Changer de modèle d'embedding sans benchmark peut dégrader fortement un système RAG ou une mémoire d'agent.
