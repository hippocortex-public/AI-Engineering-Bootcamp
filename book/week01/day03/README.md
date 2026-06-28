# Semaine 1 — Jour 3 — Transformer et Attention

## Position dans la semaine

La Semaine 1 vise à comprendre le fonctionnement des LLM. Le Jour 3 introduit l'architecture Transformer et le mécanisme d'attention, après les embeddings et les premiers réseaux neuronaux, et avant les tokens, BPE et fenêtre de contexte.

## Objectif du jour

Comprendre pourquoi l'attention a rendu possible les modèles de langage modernes, comment fonctionne une couche Transformer et comment raisonner comme un AI Engineer sur les compromis d'architecture.

## Livrables

- `learning_objectives.md`
- `chapter.md`
- `exercises.md`
- `corriges/exercises_solutions.md`
- `interview.md`
- `challenge.md`
- `corriges/challenge_solution.md`
- `references.md`
- `labs/lab_attention_from_scratch.md`
- `labs/scaled_dot_product_attention.py`
- `labs/tiny_transformer_block.py`
- `diagrams/transformer_encoder.mmd`
- `diagrams/attention_pipeline.mmd`
- `assets/toy_sequence.json`
- `notebooks/week01/day03/day03_transformer_attention.ipynb`

## Compétence construite

À la fin de cette journée, l'apprenant sait expliquer et implémenter une attention scaled dot-product simplifiée, relier cette brique au Transformer, et identifier les limites pratiques liées au coût quadratique de l'attention.

## Pré-requis

- Vecteurs et produits scalaires
- Notion d'embedding
- Bases Python
- Notions minimales sur NumPy

## Résultat attendu

Un mini-lab exécutable permettant de calculer une matrice d'attention, d'observer ses poids et de construire un bloc Transformer simplifié.
