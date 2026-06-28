# Exercices — Tokens, BPE et fenêtre de contexte

## Exercice 1 — Identifier les tokens conceptuels

Pour chaque texte, proposez un découpage plausible en tokens ou sous-mots.

1. `AI Engineering`
2. `tokenization`
3. `reusable_components`
4. `L'utilisateur demande une réponse courte.`
5. `context_window_overflow`

Questions :

- Quels éléments risquent d’être découpés ?
- Les underscores sont-ils nécessairement séparés ?
- Pourquoi les espaces peuvent-ils changer le résultat ?

## Exercice 2 — Compter des paires BPE

Corpus :

```text
low
lower
lowest
```

Découpage initial :

```text
l o w </w>
l o w e r </w>
l o w e s t </w>
```

1. Listez les paires adjacentes.
2. Comptez leurs fréquences.
3. Identifiez la première fusion probable.
4. Appliquez cette fusion au corpus.

## Exercice 3 — Implémenter une fusion

Écrivez une fonction Python :

```python
def merge_pair(tokens: list[str], pair: tuple[str, str], replacement: str) -> list[str]:
    ...
```

La fonction doit remplacer les occurrences adjacentes de `pair` par `replacement`.

Exemple :

```python
merge_pair(["l", "o", "w"], ("l", "o"), "lo")
# ["lo", "w"]
```

## Exercice 4 — Budget de contexte

Un modèle accepte 16 000 tokens.

Votre prompt contient :

- instructions système : 700 tokens ;
- historique conversationnel : 4 200 tokens ;
- documents : 8 900 tokens ;
- question utilisateur : 300 tokens.

Vous voulez réserver 1 500 tokens pour la réponse.

Questions :

1. Le prompt passe-t-il dans la fenêtre ?
2. Combien reste-t-il ?
3. Quelle stratégie proposez-vous si le budget est dépassé ?

## Exercice 5 — Diagnostic production

Une équipe observe :

- coût élevé ;
- latence élevée ;
- réponses moins précises ;
- prompts contenant beaucoup d’historique ancien.

Questions :

1. Quel lien avec la fenêtre de contexte ?
2. Quelles métriques faut-il ajouter ?
3. Quelle première correction proposer ?
