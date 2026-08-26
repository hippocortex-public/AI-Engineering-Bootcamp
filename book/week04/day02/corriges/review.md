# Review formateur — Jour 2

## Intention pédagogique

Cette journée transforme l’idée d’agent en composant logiciel. Les apprenants doivent sortir du réflexe “un agent = un prompt + un appel API” et comprendre qu’un agent de framework doit avoir un contrat stable.

## Points à insister

- Un agent ne doit pas dépendre directement d’un fournisseur.
- La sortie structurée est indispensable pour l’orchestration.
- Les guardrails simples clarifient le contrat.
- Le faux modèle n’est pas un raccourci : c’est une stratégie de test professionnelle.
- Les tools ne sont pas encore implémentés ; ils arrivent au jour 3.

## Démonstration conseillée

1. Exécuter `agent_abstraction.py`.
2. Montrer le `AgentResult`.
3. Modifier l’entrée pour qu’elle soit vide.
4. Montrer le statut `blocked`.
5. Lancer les tests.
6. Ajouter un second agent avec un autre faux modèle.

## Erreurs fréquentes

- Mettre l’appel SDK directement dans l’agent.
- Retourner uniquement du texte.
- Confondre agent et workflow.
- Ajouter une mémoire avant d’avoir un contrat d’exécution clair.
- Introduire les tools trop tôt.

## Critères de maîtrise

L’apprenant maîtrise la journée s’il peut :

- expliquer la responsabilité d’un agent ;
- écrire un agent testable ;
- injecter un model client ;
- retourner une sortie standardisée ;
- justifier pourquoi le framework évoluera mieux avec ce design.

## Préparation jour 3

Le jour 3 ajoutera un `Tool Registry`. L’enseignant peut terminer par cette question :

> Où brancher des tools sans casser l’abstraction Agent construite aujourd’hui ?

La réponse attendue : via une dépendance ou un registre injecté, sans rendre l’agent responsable du stockage global des tools.
