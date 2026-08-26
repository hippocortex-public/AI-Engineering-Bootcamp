# Review formateur — Sharing State

## Objectif de la revue

Vérifier que les apprenants comprennent que le shared state est un contrat d'architecture et non un simple dictionnaire global.

## Points à vérifier

- L'apprenant distingue local state, conversation state, shared state et memory.
- Il comprend pourquoi une écriture doit être versionnée.
- Il sait expliquer un conflit compare-and-set.
- Il comprend l'intérêt d'un patch atomique.
- Il ne transmet pas tout l'état lors d'un handoff.
- Il filtre les données privées.
- Il sait exploiter un event log.
- Il sait relier le shared state à MCP sans les confondre.

## Questions de relance

- Que se passe-t-il si deux agents écrivent sur `plan.next_step` ?
- Pourquoi le reviewer n'a-t-il pas besoin des notes privées du triage ?
- Que mettriez-vous dans Redis ? Que mettriez-vous dans PostgreSQL ?
- Quelles clés exposeriez-vous via MCP Resources ?
- Que supprimeriez-vous à la fin d'un workflow ?

## Erreurs fréquentes

1. Utiliser une variable globale partagée.
2. Confondre shared state et long-term memory.
3. Oublier les versions.
4. Oublier les permissions.
5. Mettre tout le journal d'événements dans le prompt.
6. Exposer des brouillons comme faits validés.
7. Rendre le handoff trop volumineux.

## Critères de validation

Un apprenant maîtrise la journée s'il peut :

- expliquer le modèle ;
- implémenter le store ;
- passer les tests ;
- justifier les règles de visibilité ;
- diagnostiquer un conflit ;
- produire un handoff minimal ;
- proposer une évolution production réaliste.

## Proposition d'amélioration

Ajouter ultérieurement un exercice optionnel avec Redis ou SQLite pour montrer la persistance transactionnelle, sans modifier la structure officielle de la journée.
