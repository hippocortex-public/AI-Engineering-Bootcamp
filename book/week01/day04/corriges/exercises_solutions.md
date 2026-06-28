# Corrigés — Exercices Jour 4

## Exercice 1 — Solution indicative

1. `AI Engineering` peut être découpé en `AI` et ` Engineering`, ou en unités plus petites selon le tokenizer.
2. `tokenization` peut devenir `token`, `ization`.
3. `reusable_components` peut être découpé autour de `re`, `usable`, `_`, `components`, ou différemment selon le vocabulaire.
4. La phrase française peut avoir des découpages variables, notamment autour de l’apostrophe dans `L'utilisateur`.
5. `context_window_overflow` peut être découpé par fragments fréquents : `context`, `_`, `window`, `_`, `overflow`.

Les espaces peuvent être intégrés dans les tokens. Un token précédé d’un espace peut donc être différent du même texte sans espace.

## Exercice 2 — Solution

Corpus initial :

```text
l o w </w>
l o w e r </w>
l o w e s t </w>
```

Paires :

- `(l, o)` : 3
- `(o, w)` : 3
- `(w, </w>)` : 1
- `(w, e)` : 2
- `(e, r)` : 1
- `(r, </w>)` : 1
- `(e, s)` : 1
- `(s, t)` : 1
- `(t, </w>)` : 1

La première fusion probable est `(l, o)` ou `(o, w)`, ex æquo. Un algorithme déterministe doit définir une règle de tie-break.

Après fusion `(l, o) -> lo` :

```text
lo w </w>
lo w e r </w>
lo w e s t </w>
```

## Exercice 3 — Solution

```python
def merge_pair(tokens: list[str], pair: tuple[str, str], replacement: str) -> list[str]:
    result = []
    i = 0
    while i < len(tokens):
        if i < len(tokens) - 1 and (tokens[i], tokens[i + 1]) == pair:
            result.append(replacement)
            i += 2
        else:
            result.append(tokens[i])
            i += 1
    return result
```

## Exercice 4 — Solution

Calcul :

```text
prompt = 700 + 4200 + 8900 + 300 = 14100
prompt + sortie = 14100 + 1500 = 15600
fenêtre = 16000
reste = 400
```

Le prompt passe, mais avec une marge faible. En production, c’est risqué car l’estimation peut être approximative.

Stratégies :

- réduire les documents ;
- résumer l’historique ;
- réserver une marge plus grande ;
- limiter la réponse ;
- sélectionner uniquement les chunks les plus pertinents.

## Exercice 5 — Solution

Le problème est probablement lié à une injection excessive de contexte. Plus le prompt est long, plus le coût et la latence augmentent. Le bruit contextuel peut aussi réduire la précision.

Métriques à ajouter :

- tokens d’entrée ;
- tokens de sortie ;
- coût par requête ;
- latence modèle ;
- nombre de messages historiques injectés ;
- nombre de chunks injectés ;
- taux de dépassement de budget.

Première correction :

- limiter l’historique aux derniers échanges utiles ;
- résumer l’historique ancien ;
- appliquer un budget de contexte avant appel modèle.
