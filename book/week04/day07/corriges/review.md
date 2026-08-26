# Review formateur — Jour 7

## Objectif de la revue

Vérifier que les apprenants comprennent l'intégration d'un framework d'agents comme un problème d'architecture logicielle, pas comme une simple accumulation de prompts.

## Points à vérifier

- L'apprenant sait expliquer le rôle de chaque couche.
- L'apprenant sait justifier le registre d'outils.
- L'apprenant sait distinguer mémoire, état et historique.
- L'apprenant trace les décisions importantes.
- L'apprenant refuse les actions sensibles sans approbation.
- L'apprenant écrit des tests sur les erreurs, pas seulement sur les succès.

## Erreurs fréquentes

### Coupler agent et outils

Certains apprenants appellent directement les fonctions depuis l'agent. Cela contourne les permissions et rend le système difficile à auditer.

### Oublier les traces

Un framework sans trace est très difficile à exploiter.

### Confondre blocage et échec

Une action sensible sans approbation n'est pas forcément un échec technique. C'est souvent un blocage attendu.

### Rendre le workflow implicite

Un workflow caché dans une suite de `if` devient difficile à maintenir.

## Critères de validation

Un rendu est satisfaisant si :

- les tests passent ;
- le résultat est JSON-sérialisable ;
- les responsabilités sont séparées ;
- les outils sensibles sont protégés ;
- la trace est exploitable ;
- le workflow est déterministe.

## Propositions d'amélioration

Sans modifier les spécifications, on peut proposer aux apprenants avancés :

- d'ajouter un exporter OpenTelemetry ;
- de rendre le runner asynchrone ;
- de charger les workflows depuis un fichier YAML ;
- de brancher une mémoire persistante SQLite ;
- d'ajouter un adaptateur FastAPI lors de la semaine 5.
