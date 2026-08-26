# Exercices — Architectures multi-agents

## Exercice 1 — Identifier le bon pattern

Choisir le pattern adapté :

1. Router une demande client vers facturation, technique ou remboursement.
2. Produire un rapport final à partir de trois analyses spécialisées.
3. Vérifier qu’une réponse respecte une politique interne.
4. Transférer la conversation à un spécialiste juridique.
5. Analyser un document sous trois angles indépendants.

Justifier chaque réponse.

## Exercice 2 — Définir des responsabilités

Concevoir une architecture multi-agents pour une plateforme SaaS B2B avec :

- facturation ;
- bug applicatif ;
- demande de fonctionnalité ;
- sécurité ;
- résiliation.

Inclure un router, au moins trois spécialistes et un reviewer.

## Exercice 3 — Contrat d’agent

Écrire un contrat JSON pour `security_specialist` avec :

- nom ;
- responsabilité ;
- entrées ;
- sortie ;
- outils ;
- conditions de handoff ;
- modes d’échec.

## Exercice 4 — État partagé

Classer ces éléments :

- toujours partagé ;
- partagé sous condition ;
- jamais partagé.

Éléments :

1. message utilisateur courant ;
2. historique complet ;
3. décision de routage ;
4. mémoire long terme ;
5. résultat intermédiaire ;
6. données sensibles ;
7. trace d’exécution ;
8. raisonnement interne.

## Exercice 5 — Limites du multi-agent

Donner trois cas où il vaut mieux garder un agent unique. Expliquer le risque créé par le multi-agent.

## Exercice 6 — Lab

Exécuter :

```bash
python multi_agent_architecture.py
python test_multi_agent_architecture.py
```

Puis ajouter un spécialiste `security` et un test de routage.
