# Objectifs pédagogiques

## Objectifs principaux

À la fin de cette journée, l’apprenant sera capable de :

1. distinguer logging, métriques, traces et alerting ;
2. identifier les métriques spécifiques aux systèmes IA ;
3. instrumenter une API FastAPI avec des métriques de latence, d’erreurs et de volume ;
4. exposer un endpoint `/metrics` lisible par une plateforme de supervision ;
5. calculer une estimation de coût basée sur les tokens ;
6. détecter des conditions d’alerte simples ;
7. protéger les logs contre l’exposition de données sensibles ;
8. tester la logique de monitoring sans dépendre d’un fournisseur LLM.

## Compétences AI Engineering

Cette journée développe les compétences suivantes :

- concevoir un contrat d’observabilité pour une API IA ;
- rendre un service IA exploitable par une équipe production ;
- séparer les métriques système des métriques modèle ;
- transformer des événements applicatifs en signaux actionnables ;
- écrire du code de monitoring testable ;
- raisonner en coût, latence, fiabilité et qualité.

## Notions clés

- Observabilité
- Logging structuré
- Métriques
- Traces
- SLO
- Error rate
- P95 latency
- Token usage
- Cost monitoring
- Model quality signal
- Alerting
- Redaction
- Runbook

## Critères de réussite

La journée est réussie si l’apprenant peut :

- ajouter une métrique sans modifier toute l’API ;
- expliquer pourquoi `200 OK` ne suffit pas à mesurer la santé d’un système IA ;
- calculer une estimation de coût par requête ;
- écrire une règle d’alerte compréhensible ;
- filtrer les données sensibles avant journalisation ;
- exécuter les tests du lab avec succès.
