# Objectifs pédagogiques

## Objectifs principaux

À la fin de ce jour, l'apprenant doit être capable de :

1. expliquer le rôle de l'attention dans un modèle de langage ;
2. décrire les matrices Query, Key et Value ;
3. calculer une attention scaled dot-product simple ;
4. interpréter une matrice de poids d'attention ;
5. expliquer pourquoi le Transformer se parallélise mieux que les architectures séquentielles ;
6. identifier le coût computationnel de l'attention ;
7. relier l'attention à des enjeux AI Engineering : latence, mémoire, contexte, observabilité.

## Compétences AI Engineering

- Lire un schéma d'architecture Transformer.
- Transformer une explication mathématique en code exécutable.
- Écrire des tests pour valider une brique algorithmique.
- Raisonner sur les compromis entre qualité, coût et performance.
- Préparer le terrain pour les notions de fenêtre de contexte du Jour 4.

## Critères de validation

L'apprenant valide la journée si :

- il sait expliquer `Q`, `K`, `V` sans réciter une définition ;
- il sait pourquoi les scores sont divisés par `sqrt(d_k)` ;
- il peut exécuter le lab sans dépendance externe lourde ;
- il comprend pourquoi l'attention complète devient coûteuse pour de longues séquences ;
- il peut distinguer attention, self-attention, multi-head attention et bloc Transformer.
