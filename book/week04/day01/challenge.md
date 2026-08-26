# Challenge — Concevoir l'architecture d'un assistant IA mono-framework

## Contexte

Tu dois concevoir le socle d'un mini-framework destiné à construire un assistant IA pour une équipe support.

L'assistant devra plus tard :

- comprendre une demande utilisateur ;
- appeler des outils internes ;
- conserver un état de tâche ;
- escalader les cas sensibles ;
- tracer chaque étape ;
- être testable sans appel modèle réel.

## Mission

Produis une proposition d'architecture composée de :

1. une liste de composants ;
2. la responsabilité de chaque composant ;
3. les dépendances entre composants ;
4. trois invariants ;
5. deux décisions d'architecture ;
6. un diagramme Mermaid ;
7. un plan d'implémentation en quatre étapes.

## Contraintes

- Aucun composant ne doit tout faire.
- Le modèle doit être remplaçable.
- Les outils doivent être déclarés hors du runner.
- L'observabilité ne doit pas modifier l'exécution.
- La mémoire ne doit pas être un dictionnaire global.
- Les actions sensibles doivent être explicitement représentées.

## Critères de réussite

Le challenge est réussi si :

- l'architecture est compréhensible sans lire le code ;
- les dépendances sont cohérentes ;
- les responsabilités ne se chevauchent pas excessivement ;
- les invariants sont vérifiables ;
- le diagramme reflète le texte ;
- le plan prépare les jours 2 à 7.
