# Corrigé des exercices

## Exercice 1 — Décrire le port

Entrée : événement validé. Sortie : category parmi billing/general et draft non vide borné. TemporaryFailure autorise une reprise; InvalidEvent arrête le traitement automatique. Les bugs inattendus restent visibles.

## Exercice 2 — Provoquer une sortie invalide

validate_proposal détecte les champs manquants. Le job va en dead_letter dès la première tentative; aucune proposition exploitable n’est stockée.

## Exercice 3 — Étudier une injection

Le texte n’est pas une commande du moteur. Le générateur n’a pas de port de publication. decide impose une identité, un hash et un état autorisé. Un prompt peut compléter ces contrôles sans les remplacer.
