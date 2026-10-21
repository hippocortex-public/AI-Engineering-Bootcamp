# Corrigé des exercices

## Exercice 1 — Calculer le budget

Appels à 1000,1002,1006 si le scheduler est exécuté exactement aux échéances. Après le troisième échec, dead_letter. Un scheduler plus lent décale les appels.

## Exercice 2 — Classer les erreurs

Timeout : potentiellement transitoire; catégorie inconnue : permanent; token invalide : configuration à corriger, pas reprise aveugle; TypeError : bug à laisser visible.

## Exercice 3 — Analyser un crash externe

L’outbox conserve l’intention et la progression locale. Elle ne prouve pas que le destinataire n’a rien reçu. Réutiliser une clé stable chez le destinataire ou réconcilier; sinon doublon possible.
