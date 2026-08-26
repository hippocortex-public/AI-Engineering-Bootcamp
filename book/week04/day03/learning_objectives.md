# Objectifs d’apprentissage

À la fin de cette journée, l’apprenant saura :

## Objectifs conceptuels

- expliquer pourquoi un agent ne doit pas appeler directement des fonctions métier non contrôlées ;
- distinguer `ToolDefinition`, `ToolRegistry`, `ToolContext` et `ToolResult` ;
- décrire le cycle `discover → validate → authorize → execute → trace` ;
- comprendre les risques liés aux tools sensibles ;
- justifier l’usage d’un schéma d’entrée explicite ;
- séparer description publique d’un outil et handler Python interne.

## Objectifs pratiques

- implémenter un registre d’outils en Python ;
- enregistrer un tool avec son schéma d’entrée ;
- lister les tools disponibles pour un agent ;
- valider des arguments avant appel ;
- appliquer une politique de scope et d’approbation humaine ;
- capturer une exception de handler sans casser l’agent ;
- exporter un manifest JSON sérialisable.

## Objectifs AI Engineering

- concevoir une frontière sûre entre modèle et application ;
- préparer l’intégration future avec un runner, un workflow engine et l’observabilité ;
- produire du code testable sans dépendre d’une clé API ;
- raisonner en termes de contrats, d’invariants et de surfaces d’attaque.
