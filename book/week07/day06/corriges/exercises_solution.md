# Corrigé des exercices

## Exercice 1 — Hash ou signature ?

Il lie la décision au JSON exact du brouillon courant. Il ne prouve pas l’identité, ne chiffre pas le texte et ne rend pas le journal inviolable.

## Exercice 2 — Éprouver les gardes

Mauvais hash :409; date expirée :409; mauvais rôle HTTP :401. Aucun de ces cas ne crée une publication.

## Exercice 3 — Traiter le refus

Le refus est une décision métier valide. Une reprise automatique chercherait à contourner le choix humain. Une nouvelle proposition exige un nouveau parcours explicite.
