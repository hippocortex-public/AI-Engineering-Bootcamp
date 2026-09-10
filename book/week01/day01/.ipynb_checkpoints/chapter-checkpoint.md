# Day 1 — L'histoire des modèles de langage

## Question centrale

Pourquoi les LLM existent-ils ?

## Objectifs

À la fin de cette journée, vous serez capable de :

- expliquer les limites des systèmes à règles ;
- comprendre pourquoi les statistiques ont remplacé les règles explicites ;
- expliquer les limites des n-grammes ;
- comprendre pourquoi le problème central est devenu la gestion du contexte long.

## 1. Avant les LLM : les règles

Les premiers systèmes conversationnels reposaient sur des règles écrites à la main.

Exemple :

```text
SI l'utilisateur dit "je suis triste"
ALORS répondre "Pourquoi êtes-vous triste ?"
```

Cette approche est prévisible mais ne passe pas à l'échelle.

## 2. ELIZA

ELIZA est un chatbot historique fondé sur des transformations de texte.

Il ne comprenait pas réellement le langage. Il reconnaissait des motifs et produisait des réponses associées.

## 3. Les systèmes experts

Les systèmes experts ont tenté de capturer explicitement les connaissances humaines.

```text
SI fièvre ET toux ALORS suspicion de grippe
```

Le problème principal était la maintenance : plus le système grandit, plus les règles interagissent de manière difficile à maîtriser.

## 4. Les modèles statistiques

Les chercheurs ont progressivement remplacé les règles manuelles par des probabilités apprises sur des corpus.

Le modèle ne dit plus :

> Cette règle s'applique.

Il dit :

> Dans les données observées, cette suite de mots est probable.

## 5. Les n-grammes

Un n-gramme prédit le mot suivant à partir des mots précédents.

Exemple :

```text
Je vais boire un ...
```

Le modèle peut estimer :

- café ;
- thé ;
- verre.

## 6. Limite principale

Les n-grammes utilisent une fenêtre courte. Ils ne comprennent pas les dépendances longues.

Exemple :

```text
Le chat que j'ai adopté il y a trois ans dort sur le canapé.
```

Le modèle doit conserver l'information liée au sujet.

## 7. Problème central

La question devient :

> Comment conserver une information pertinente sur une longue séquence de texte ?

Cette question mènera aux réseaux neuronaux, aux embeddings, aux RNN, aux LSTM, puis aux Transformers.

## Synthèse

Les LLM sont le résultat d'une longue progression :

```text
Règles -> statistiques -> réseaux neuronaux -> attention -> transformers -> agents
```

Chaque étape répond à une limite de l'étape précédente.
