# Corrigé — Questions d'entretien

## Question 1

Les logs seuls ne reconstruisent pas la structure d'exécution. Un agent peut appeler plusieurs outils, changer de plan, consulter la mémoire et déclencher des guardrails. Il faut une trace avec spans parent/enfant pour comprendre le chemin exact.

## Question 2

Une trace représente l'opération complète. Un span représente une sous-opération dans cette trace, avec durée, statut, attributs et parent éventuel.

## Question 3

Un appel d'outil doit être instrumenté comme un span de type `tool`, avec :

- nom de l'outil ;
- arguments redacted ;
- début/fin ;
- statut ;
- résultat résumé ;
- erreur éventuelle ;
- événement de validation.

## Question 4

Les risques principaux sont :

- fuite de données personnelles ;
- exposition de secrets ;
- capture de prompts internes ;
- stockage excessif ;
- accès non contrôlé aux traces ;
- confusion entre logs de debug et données exploitables en production.

## Question 5

Appliquer une redaction par défaut basée sur :

- noms de clés sensibles ;
- patterns ;
- classification des champs ;
- allowlist des attributs autorisés ;
- option explicite pour inclure des données sensibles en local.

## Question 6

On suit la trace :

1. intention classifiée ;
2. contexte utilisé ;
3. outils appelés ;
4. résultats obtenus ;
5. erreurs ;
6. guardrails ;
7. synthèse finale.

On identifie ainsi si l'erreur vient du contexte, de l'outil, du modèle ou du workflow.

## Question 7

Signaux utiles :

- taux d'échec ;
- latence moyenne ;
- nombre d'appels outils ;
- taux de guardrail ;
- coût estimé ;
- nombre de clarifications ;
- score d'évaluation ;
- taux de fallback.

## Question 8

Le tool registry et le workflow engine sont les principales sources d'effets observables : appels externes, retries, blocages, transitions de statut. Sans instrumentation à ce niveau, le framework devient opaque.

## Question 9

L'observabilité doit être non intrusive :

- pas d'effets de bord fonctionnels ;
- exceptions d'observabilité isolées ;
- export asynchrone ou tolérant ;
- redaction déterministe ;
- tests garantissant que le comportement métier ne dépend pas du tracing.

## Question 10

Exporter :

- traces ;
- spans ;
- événements ;
- métriques ;
- attributs redacted ;
- erreurs ;
- durées ;
- relations parent/enfant ;
- métadonnées de service.
