# Corrigé — Questions d’entretien

## Question 1

Le taux de disponibilité HTTP ne suffit pas, car une application IA peut retourner `200 OK` tout en produisant une réponse vide, incorrecte, hallucinated, trop coûteuse ou non conforme au besoin métier. Il faut donc monitorer la qualité, le coût, les tokens, les refus, les réponses vides et les signaux d’usage en plus des statuts HTTP.

## Question 2

Les logs décrivent des événements individuels. Les métriques agrègent des mesures numériques dans le temps. Les traces décrivent le parcours d’une requête entre plusieurs composants. Les trois sont complémentaires : les métriques détectent, les logs expliquent, les traces localisent.

## Question 3

La moyenne masque les extrêmes. Une API peut avoir une latence moyenne acceptable tout en imposant une mauvaise expérience à 5 % des utilisateurs. Le P95 montre la latence sous laquelle 95 % des requêtes se terminent. Il est donc plus représentatif des lenteurs réellement ressenties.

## Question 4

On monitore le coût en collectant les tokens d’entrée et de sortie, le modèle utilisé, les retries, les appels d’outils et les cache hits. On applique ensuite une formule de coût par modèle. Les coûts doivent être agrégés par route, utilisateur, tenant, environnement et période.

## Question 5

Il ne faut pas logger les secrets, clés API, tokens d’accès, emails, numéros de téléphone, données personnelles, prompts client confidentiels, outputs sensibles ou informations métier privées. Quand une information est utile au diagnostic, il faut préférer un hash, une longueur, une catégorie ou une version redacted.

## Question 6

Une alerte utile est actionnable, reliée à un seuil clair, associée à une sévérité, documentée par un runbook et suffisamment rare pour éviter la fatigue d’alerte. Elle doit indiquer quoi vérifier et quelle mitigation appliquer.

## Question 7

On diagnostique une hausse de latence en comparant la latence par route, modèle, tenant et dépendance. Il faut vérifier le fournisseur LLM, Redis, PostgreSQL, les retries, la taille des prompts, le nombre d’appels d’outils, les changements récents de déploiement et la saturation infrastructure.

## Question 8

Le code de monitoring doit être testé car il influence les décisions opérationnelles. Une erreur dans le calcul du taux d’erreur, du P95 ou du coût peut masquer un incident ou déclencher de fausses alertes. Tester ce code renforce la fiabilité production.
