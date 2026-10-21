# Corrigé des exercices

## Exercice 1 — Écrire la machine à états

received et retry vont vers awaiting_review, retry ou dead_letter. awaiting_review va vers published, rejected ou expired. Les décisions et le replay ont leurs propres gardes.

## Exercice 2 — Étudier une panne

La génération peut se répéter et coûter deux appels. Aucun effet de publication locale n’a encore eu lieu. Un générateur qui effectuerait une écriture externe exigerait une garantie supplémentaire.

## Exercice 3 — Séparer les identifiants

event_id identifie une entrée métier stable entre livraisons. Une exécution n8n identifie un passage technique et peut regrouper plusieurs jobs ou être répétée.
