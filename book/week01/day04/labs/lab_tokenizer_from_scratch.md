# Lab — Tokenizer BPE pédagogique from scratch

## Objectif

Implémenter un tokenizer BPE minimal en Python standard.

## Étapes

1. Charger un corpus.
2. Découper chaque mot en caractères.
3. Compter les paires adjacentes.
4. Fusionner la paire la plus fréquente.
5. Répéter pendant `n` merges.
6. Encoder une nouvelle phrase.
7. Décoder la représentation.

## Commande

```bash
python book/week01/day04/labs/bpe_tokenizer.py
```

## Questions d’observation

- Que se passe-t-il quand le nombre de merges augmente ?
- Quels tokens apparaissent en premier ?
- Le tokenizer généralise-t-il aux mots absents du corpus ?
- Pourquoi l’algorithme de tie-break est-il important ?
