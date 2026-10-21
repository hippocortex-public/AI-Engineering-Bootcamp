# Corrigé des exercices

## Exercice 1 — Établir les critères d’acceptation

Pas de publication sans approbation; aucun effet sur doublon identique; collision rejetée; validation expirée bloquée; reprise bornée et dead letter observable. Ajouter authentification et persistance selon le périmètre.

## Exercice 2 — Lire les compteurs

Pas nécessairement : les humains peuvent ne pas avoir décidé. Vérifier l’âge, le délai attendu et le nombre d’entrées. Un compteur seul ne distingue pas attente normale et blocage.

## Exercice 3 — Choisir une prochaine évolution

D’abord identité et autorisation individuelles et traitement des effets externes; ensuite concurrence et exploitation selon le débit. Justifier avec les risques et contraintes réels, pas avec une liste d’outils.
