# Challenge — Construire un assistant support intégré

## Objectif

Étendre le mini-framework du lab pour gérer un cas de support client plus complet.

## Scénario

Un utilisateur écrit :

```text
Bonjour, ma commande est arrivée cassée. Je veux un remplacement ou un remboursement.
```

Le système doit :

1. classifier la demande ;
2. rechercher la politique de support ;
3. évaluer le risque ;
4. rédiger une réponse ;
5. préparer une action sensible sans l'exécuter ;
6. produire une trace complète ;
7. retourner un résultat JSON.

## Contraintes

- Le remboursement ne doit jamais être exécuté sans approbation.
- La mémoire utilisateur doit être consultée.
- La trace doit contenir au moins un événement par étape.
- Le résultat doit être sérialisable en JSON.
- Le workflow ne doit pas contenir de cycle.
- Les outils autorisés doivent être contrôlés par agent.

## Livrable attendu

Modifier le lab ou créer une variante qui expose :

```python
framework.run_support_case(user_id, message, approval=False)
```

La fonction doit retourner un objet contenant :

```text
status
summary
outputs
blocked_actions
trace
memory_used
```

## Critères de réussite

- Les tests passent.
- Les erreurs sont explicites.
- Le code reste lisible.
- Les responsabilités restent séparées.
- Le comportement est reproductible.
