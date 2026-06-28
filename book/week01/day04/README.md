# Semaine 1 — Jour 4 : Tokens, BPE et fenêtre de contexte

## Position dans la roadmap

- **Semaine** : 1 — Foundations of AI Engineering
- **Jour** : 4
- **Sujet** : Tokens, BPE et fenêtre de contexte
- **Objectif de semaine** : comprendre le fonctionnement des LLM
- **Mini-projet de semaine** : construire une bibliothèque Python illustrant tokenisation, embeddings et premier appel LLM

## Résultat attendu

À la fin de cette journée, l’apprenant sait expliquer pourquoi un LLM ne lit pas directement des mots, comment une chaîne de texte devient une suite d’identifiants numériques, pourquoi la fenêtre de contexte est une contrainte d’architecture, et comment estimer le coût d’un prompt avant appel modèle.

## Livrables

| Fichier | Rôle |
|---|---|
| `learning_objectives.md` | Objectifs pédagogiques |
| `chapter.md` | Cours principal |
| `exercises.md` | Exercices pratiques |
| `corriges/exercises_solutions.md` | Corrigés des exercices |
| `interview.md` | Questions d’entretien |
| `challenge.md` | Challenge de fin de journée |
| `corriges/challenge_solution.md` | Solution de référence |
| `references.md` | Références |
| `labs/lab_tokenizer_from_scratch.md` | Lab guidé |
| `labs/bpe_tokenizer.py` | Implémentation Python exécutable |
| `labs/context_window_budget.py` | Outil de budget contexte |
| `diagrams/*.mmd` | Diagrammes Mermaid |
| `assets/sample_corpus.txt` | Corpus minimal |
| `notebooks/week01/day04/day04_tokens_bpe_context.ipynb` | Notebook généré à partir du contenu Markdown |

## Pré-requis

- Avoir terminé J1 à J3.
- Comprendre la représentation vectorielle de base.
- Savoir exécuter un script Python.
- Connaître les grandes étapes du Transformer.

## Commandes utiles

Depuis la racine du dépôt généré :

```bash
python book/week01/day04/labs/bpe_tokenizer.py
python book/week01/day04/labs/context_window_budget.py
python -m pytest tests/week01/day04
```

## Résumé technique

Un LLM traite des **tokens**, pas des caractères ni des mots. La tokenisation transforme un texte en unités numériques stables. BPE, pour Byte Pair Encoding, apprend des fusions fréquentes à partir d’un corpus pour représenter efficacement des morceaux de texte. La fenêtre de contexte limite le nombre total de tokens que le modèle peut prendre en entrée et produire en sortie. En production, cette limite devient un sujet d’architecture : découpage, compression, sélection de contexte, coût, latence et qualité.
