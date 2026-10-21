# Corrigé des exercices

## Exercice 1 — Dessiner une enveloppe

L’exemple assets/event.json est valide. schema_version:2 est refusé. Un schéma version 2 doit avoir un consommateur capable de le comprendre et une migration explicite.

## Exercice 2 — Simuler une livraison répétée

Premier POST:202; répétition identique:200; contenu différent:409. Le premier job reste inchangé.

## Exercice 3 — Analyser deux identifiants

Pas automatiquement. Il peut s’agir de deux faits distincts. Une règle métier de supersession ou de regroupement par ticket est nécessaire avant de fusionner.
