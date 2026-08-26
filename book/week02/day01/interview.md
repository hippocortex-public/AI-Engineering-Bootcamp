# Questions d’entretien — Architecture d’un agent

## Questions courtes

1. Quelle différence fais-tu entre un modèle de langage et un agent ?
2. Pourquoi un agent doit-il maintenir un état ?
3. Qu’est-ce qu’un outil dans une architecture agentique ?
4. À quoi sert une trace d’exécution ?
5. Quelle est la différence entre mémoire et état ?
6. Pourquoi séparer la politique de décision de l’exécution des outils ?
7. Quels risques apparaissent lorsqu’un agent peut appeler des outils externes ?
8. Pourquoi commencer par un agent mono-agent avant de construire un système multi-agent ?

## Questions de raisonnement

### Question 1

Un agent répond parfois directement et appelle parfois un outil.

Comment structurerais-tu le code pour rendre ce comportement testable ?

### Question 2

Ton agent appelle un outil de paiement alors que l’utilisateur demandait seulement une information.

Quels composants de l’architecture faut-il inspecter en priorité ?

### Question 3

Un agent fonctionne en démonstration mais devient difficile à déboguer en production.

Quels éléments d’observabilité ajouterais-tu ?
