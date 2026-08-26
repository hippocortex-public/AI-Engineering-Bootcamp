# Objectifs pédagogiques

À la fin de cette journée, l'apprenant doit être capable de :

## Comprendre

- distinguer logs, traces, spans, événements et métriques ;
- expliquer pourquoi l'observabilité est plus critique pour les agents que pour une API classique ;
- identifier les signaux utiles pour analyser une boucle agentique ;
- comprendre les risques de fuite de données sensibles dans les traces ;
- différencier observabilité de debugging manuel.

## Concevoir

- concevoir un modèle de trace pour un agent ;
- structurer les spans autour des étapes d'exécution ;
- relier un appel d'outil à une trace parent ;
- définir des événements métier utiles ;
- choisir des métriques de fiabilité et de coût ;
- intégrer une politique de redaction.

## Implémenter

- créer une trace ;
- créer des spans imbriqués ;
- capturer une exception sans perdre le contexte ;
- exporter les traces en JSON ;
- calculer des métriques de latence ;
- générer un rapport de santé exploitable.

## AI Engineering

- instrumenter un mini-framework d'agents ;
- rendre un run agentique auditable ;
- préparer l'intégration future avec un système de monitoring ;
- produire des traces lisibles par un humain et par une machine.
