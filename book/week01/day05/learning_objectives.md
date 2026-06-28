# Objectifs pédagogiques — Jour 5 : Prompt Engineering

## Objectifs principaux

À la fin de cette journée, l'apprenant doit être capable de :

1. Expliquer pourquoi le prompt engineering est une discipline d'ingénierie et non une simple rédaction d'instructions.
2. Décomposer un prompt en blocs : rôle, tâche, contexte, contraintes, exemples, format attendu et critères de qualité.
3. Concevoir un prompt stable pour une tâche de classification, d'extraction ou de génération contrôlée.
4. Utiliser des exemples few-shot de manière ciblée.
5. Réduire les ambiguïtés dans une instruction.
6. Préparer un prompt pour une intégration future avec une API LLM.
7. Évaluer un prompt sur un jeu de cas local.
8. Documenter les limites d'un prompt et les cas où il ne doit pas être utilisé.

## Compétences AI Engineering

Cette journée développe les compétences suivantes :

- traduire un besoin métier en spécification exploitable par un LLM ;
- penser en termes de contrat d'entrée/sortie ;
- écrire des prompts versionnables dans un dépôt Git ;
- concevoir des tests de non-régression pour prompts ;
- préparer la transition vers les API modernes étudiées au Jour 6.

## Critères de réussite

Un apprenant réussit la journée s'il peut :

- justifier chaque bloc d'un prompt ;
- produire au moins deux variantes d'un prompt et les comparer ;
- expliquer pourquoi un prompt peut échouer malgré une instruction claire ;
- proposer une stratégie de mitigation : format strict, exemples, garde-fous, validation applicative ;
- exécuter le lab Python et interpréter les scores obtenus.

## À ne pas confondre

Le prompt engineering ne remplace pas :

- la validation côté application ;
- les tests ;
- les politiques de sécurité ;
- l'observabilité ;
- les modèles de données ;
- les appels structurés à des outils ou fonctions.

Ces aspects seront renforcés dans les journées suivantes.
