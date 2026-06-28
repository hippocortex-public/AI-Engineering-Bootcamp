# Objectifs pédagogiques

## Objectifs principaux

À la fin de cette journée, l’apprenant doit être capable de :

1. Définir ce qu’est un token dans un système LLM.
2. Expliquer la différence entre caractères, mots, sous-mots, bytes et tokens.
3. Décrire le principe de Byte Pair Encoding.
4. Implémenter une version pédagogique de BPE en Python.
5. Encoder et décoder une chaîne simple avec un vocabulaire appris.
6. Estimer l’impact du nombre de tokens sur le coût, la latence et la mémoire.
7. Expliquer ce qu’est une fenêtre de contexte.
8. Identifier les erreurs courantes liées au dépassement de contexte.
9. Concevoir une stratégie simple de réduction de contexte.
10. Relier tokenisation, embeddings et appel LLM dans une architecture AI Engineering.

## Compétences AI Engineering

- Construire un composant de prétraitement reproductible.
- Évaluer un prompt avant exécution.
- Diagnostiquer une sortie tronquée ou incohérente liée au budget de contexte.
- Préparer les bases du Prompt Engineering de J5.
- Préparer les bases des appels API modernes de J6.

## Critères de validation

L’apprenant valide la journée s’il peut :

- exécuter `bpe_tokenizer.py` ;
- expliquer le vocabulaire produit ;
- modifier le corpus et observer l’impact sur les merges ;
- calculer un budget de contexte ;
- proposer une stratégie de réduction de prompt ;
- réussir le challenge.
