# Day 2 — Neural Language Models and Embeddings

## Question centrale

Pourquoi a-t-on eu besoin de représenter les mots sous forme de vecteurs ?

---

## 1. Le problème laissé par les n-grammes

Au Day 1, nous avons vu que les n-grammes prédisent un mot à partir d'une petite fenêtre de mots précédents.

Cette approche a permis de remplacer certaines règles explicites par des statistiques. Mais elle garde une limite importante : elle ne comprend pas la similarité entre les mots.

Pour un modèle n-gramme classique :

```text
chat
chien
voiture
banane
```

sont simplement des symboles différents.

Le modèle peut observer que certains mots apparaissent dans des contextes similaires, mais il ne possède pas encore une représentation interne riche du sens.

---

## 2. Le langage comme symboles

Dans un programme classique, un mot est une chaîne de caractères.

```python
"chat" != "chien"
```

C'est logique pour un ordinateur. Pourtant, pour un humain, `chat` et `chien` sont plus proches que `chat` et `tournevis`.

Le problème est donc le suivant :

> Comment représenter les mots de manière à refléter leurs relations sémantiques ?

---

## 3. Première tentative : le one-hot encoding

Une première solution consiste à attribuer un identifiant à chaque mot.

Supposons un vocabulaire :

```text
["chat", "chien", "voiture", "banane"]
```

On peut représenter chaque mot par un vecteur :

```text
chat    = [1, 0, 0, 0]
chien   = [0, 1, 0, 0]
voiture = [0, 0, 1, 0]
banane  = [0, 0, 0, 1]
```

Cette représentation est simple, mais elle a deux problèmes.

### Problème 1 — Dimension énorme

Si le vocabulaire contient 100 000 mots, chaque vecteur contient 100 000 dimensions.

### Problème 2 — Aucune similarité

La distance entre `chat` et `chien` est la même que la distance entre `chat` et `banane`.

Le modèle ne voit aucune proximité sémantique.

---

## 4. L'idée des embeddings

Un embedding est une représentation dense d'un mot dans un espace vectoriel.

Au lieu d'écrire :

```text
chat = [1, 0, 0, 0, 0, ...]
```

on apprend une représentation comme :

```text
chat = [0.12, -0.43, 0.87, 0.05, ...]
```

Chaque dimension ne correspond plus directement à un mot. Elle contribue à une représentation distribuée.

L'idée essentielle :

> Des mots utilisés dans des contextes similaires auront des vecteurs proches.

---

## 5. Intuition géométrique

Dans un espace vectoriel, les mots peuvent se rapprocher ou s'éloigner.

```text
chat  ───── chien

voiture ─── camion

banane ─── pomme
```

Un bon embedding doit capturer ces proximités.

Cela permet ensuite :

- la recherche sémantique ;
- la classification ;
- le clustering ;
- la mémoire vectorielle ;
- le RAG ;
- la similarité entre documents ;
- les recommandations.

---

## 6. Word2Vec

Word2Vec a popularisé l'idée d'apprendre les représentations des mots à partir de leurs contextes.

Deux grandes approches existent :

### CBOW

Prédire un mot à partir de son contexte.

```text
Le ___ dort sur le canapé.
```

### Skip-gram

Prédire le contexte à partir du mot.

```text
chat -> dort, canapé, miaule, animal
```

Le modèle apprend progressivement que certains mots apparaissent dans des contextes proches.

---

## 7. Pourquoi Word2Vec a été important

Word2Vec a montré que des régularités linguistiques pouvaient apparaître dans l'espace vectoriel.

L'exemple le plus connu est souvent formulé ainsi :

```text
king - man + woman ≈ queen
```

L'important n'est pas de retenir cette formule comme une magie mathématique. L'idée importante est que les relations entre mots peuvent être représentées par des opérations géométriques.

---

## 8. Des mots aux phrases

Les embeddings de mots sont utiles, mais les LLM modernes manipulent plutôt des tokens, des phrases, des passages et des documents.

Cela mène aux embeddings de phrases et de documents.

Exemples d'usages modernes :

- recherche sémantique ;
- détection de doublons ;
- recommandation de documents ;
- clustering de tickets support ;
- RAG ;
- mémoire longue durée d'agents.

---

## 9. Les premiers réseaux neuronaux du langage

Les embeddings ont permis aux réseaux neuronaux de manipuler le langage plus efficacement.

Au lieu de traiter des symboles bruts, le réseau reçoit des vecteurs numériques.

```text
mot -> embedding -> réseau neuronal -> prédiction
```

Cela ouvre la porte à des modèles plus puissants.

---

## 10. Les RNN

Les RNN, ou réseaux neuronaux récurrents, ont été conçus pour traiter des séquences.

Ils lisent une phrase mot par mot en maintenant un état interne.

```text
Le -> chat -> dort
```

À chaque étape, le modèle met à jour son état.

Cela permet théoriquement de retenir des informations précédentes.

---

## 11. Limites des RNN

En pratique, les RNN ont du mal à conserver des informations sur de longues séquences.

Plus une information est ancienne, plus elle risque d'être oubliée.

C'est un problème critique pour le langage.

Exemple :

```text
Le livre que j'ai acheté hier dans la grande librairie du centre-ville est ...
```

Pour prédire correctement la suite, il faut conserver des informations éloignées.

---

## 12. Les LSTM

Les LSTM ont été conçus pour mieux contrôler ce qui est retenu ou oublié.

Ils introduisent des mécanismes de portes :

- oublier ;
- retenir ;
- mettre à jour ;
- produire une sortie.

Cela améliore la mémoire à long terme, mais le traitement reste séquentiel.

---

## 13. Pourquoi les Transformers étaient nécessaires

Les RNN et LSTM lisent les séquences dans l'ordre.

Cela limite :

- la parallélisation ;
- la capacité à relier directement deux mots éloignés ;
- la vitesse d'entraînement sur de très grands corpus.

Le Transformer répondra à ces limites avec le mécanisme d'attention.

Au lieu de lire uniquement de gauche à droite, il permet à chaque token de regarder les autres tokens pertinents.

Ce sera le sujet du Day 3.

---

## 14. Lien avec l'AI Engineering moderne

Les embeddings ne sont pas seulement une ancienne étape historique.

Ils sont au cœur des systèmes modernes :

- RAG ;
- vector databases ;
- memory stores ;
- semantic search ;
- routing d'agents ;
- clustering d'intentions ;
- détection de similarité ;
- évaluation de réponses.

Un AI Backend Engineer doit donc comprendre les embeddings même s'il n'entraîne jamais un modèle.

---

## Synthèse

Le Day 2 introduit une idée centrale :

> Le langage doit être transformé en représentations numériques utiles.

Le one-hot encoding encode l'identité.

Les embeddings encodent des régularités apprises.

Les RNN et LSTM tentent ensuite de traiter les séquences, mais leurs limites mèneront au Transformer.
