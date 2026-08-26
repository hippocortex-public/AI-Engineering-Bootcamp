# Challenge — Agent explicateur testable

## Objectif

Créer un agent `ExplainerAgent` spécialisé dans l’explication de concepts AI Engineering.

L’agent doit utiliser l’abstraction du lab et respecter les contraintes suivantes :

1. nom : `explainer`;
2. instructions : expliquer simplement, avec un exemple concret ;
3. modèle logique : `fake-model`;
4. client modèle injecté ;
5. résultat standardisé ;
6. trace présente ;
7. aucun appel réseau.

## Scénario

L’utilisateur demande :

```text
Explique la différence entre agent et workflow.
```

L’agent doit produire une réponse structurée qui :

- mentionne le rôle d’un agent ;
- mentionne le rôle d’un workflow ;
- donne un exemple ;
- retourne un statut `completed`.

## Critères d’acceptation

Le challenge est réussi si :

- l’agent est instancié sans dépendance externe ;
- l’entrée est encapsulée dans un `RunContext` ;
- `run()` retourne un `AgentResult` ;
- le résultat contient au moins une trace ;
- les tests passent ;
- l’agent reste indépendant d’un fournisseur LLM réel.

## Extension optionnelle

Ajouter un deuxième agent `ReviewerAgent` qui relit la réponse de l’agent explicateur.

Ne crée pas encore de workflow complet. Le workflow engine arrive au jour 5.
