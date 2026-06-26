# Corrigés — Exercices Day 2

## Exercice 1 — Compréhension

Le one-hot encoding représente chaque mot par un vecteur très grand contenant un seul `1`.

Exemple :

```text
chat = [1, 0, 0]
chien = [0, 1, 0]
voiture = [0, 0, 1]
```

Cette représentation ne capture aucune proximité. `chat` et `chien` sont aussi éloignés que `chat` et `voiture`.

Un embedding est un vecteur dense appris à partir des données.

```text
chat = [0.12, -0.44, 0.83]
chien = [0.15, -0.39, 0.79]
```

Ici, deux mots proches peuvent avoir des vecteurs proches.

## Exercice 2 — Similarité

Groupes attendus :

- animaux : `chat`, `chien`
- véhicules : `voiture`, `camion`
- fruits : `pomme`, `banane`

Un bon espace d'embeddings devrait rapprocher les mots d'un même groupe et éloigner les groupes différents.

## Exercice 3 — AI Engineering

La recherche par mots-clés échoue lorsque l'utilisateur n'utilise pas exactement les mêmes termes que les documents.

Exemple :

- requête : "congé maladie"
- document : "absence pour raison médicale"

Une recherche vectorielle peut rapprocher ces concepts même sans correspondance exacte.

## Exercice 4 — Architecture

Pour une mémoire longue durée d'agent :

- transformer en embeddings les préférences utilisateur, résumés de conversation, faits métier validés ;
- stocker dans une base vectorielle comme Qdrant, Weaviate ou Pinecone ;
- récupérer par similarité selon la requête courante ;
- surveiller la fraîcheur, la confidentialité, la dérive, les doublons et les erreurs de mémorisation.

Point important : on ne stocke pas toute la conversation brute sans filtrage.
