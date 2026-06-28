# Interview — Jour 5 : Prompt Engineering

## Questions fondamentales

### 1. Pourquoi dit-on qu'un prompt est une interface ?

Un prompt est une interface parce qu'il définit comment une application transmet une intention à un modèle. Comme une API, il doit préciser l'entrée, le comportement attendu, la sortie et les limites.

### 2. Quelle est la différence entre zero-shot et few-shot prompting ?

Le zero-shot donne uniquement l'instruction. Le few-shot ajoute des exemples pour clarifier le pattern attendu. Le few-shot peut améliorer la stabilité mais consomme plus de contexte.

### 3. Pourquoi un prompt long peut-il être moins performant ?

Un prompt long peut introduire des contradictions, diluer l'instruction principale, augmenter le coût et réduire la place disponible pour les données utiles.

### 4. Comment limiter le risque de prompt injection ?

Il faut séparer clairement les instructions des données utilisateur, rappeler que l'entrée est non fiable, éviter de placer des instructions critiques dans des zones contrôlées par l'utilisateur et valider la sortie côté application.

### 5. Pourquoi la validation applicative reste obligatoire ?

Un LLM peut produire une sortie incorrecte même avec un bon prompt. La validation applicative permet de vérifier le schéma, les valeurs autorisées, les contraintes métier et les risques de sécurité.

## Questions d'architecture

### 6. Où stocker les prompts dans un projet professionnel ?

Les prompts doivent être versionnés dans le dépôt, idéalement sous forme de templates lisibles, testables et revus comme du code.

### 7. Comment tester un prompt ?

On peut créer un dataset de cas représentatifs, définir les sorties attendues, exécuter le prompt avec un modèle ou simulateur, puis comparer les résultats avec des métriques simples.

### 8. Quand faut-il passer d'un prompt libre à une sortie structurée ?

Dès que la sortie est consommée par du code. Une sortie structurée réduit les erreurs d'intégration et prépare la validation automatique.

### 9. Quel est le lien entre prompt engineering et tool calling ?

Le prompt peut préparer la décision d'appeler un outil, mais l'appel lui-même doit être contrôlé par un mécanisme structuré. Le prompt ne doit pas être le seul garde-fou.

### 10. Comment gérer l'évolution d'un prompt en production ?

Il faut versionner le prompt, tracer les changements, exécuter des tests de non-régression, mesurer les impacts et prévoir un rollback.

## Question de synthèse

### 11. Quelle est la limite principale du prompt engineering ?

Le prompt engineering influence le comportement du modèle, mais ne fournit pas de garantie absolue. L'AI Engineering consiste à combiner prompts, validation, tests, outils, observabilité et architecture logicielle.
