# Objectifs pédagogiques — Jour 6

## Objectif principal

Comprendre comment les API modernes de modèles de langage transforment un LLM en composant logiciel intégrable.

## Compétences visées

### Compréhension

L'apprenant doit pouvoir expliquer :

- pourquoi les API modernes séparent les instructions, l'entrée utilisateur, les outils et le format de sortie ;
- pourquoi une sortie JSON n'est pas automatiquement une sortie fiable ;
- comment un modèle peut demander l'exécution d'un outil sans l'exécuter lui-même ;
- pourquoi l'application reste responsable de la validation, de l'autorisation et des effets de bord.

### Pratique

L'apprenant doit pouvoir implémenter :

- un objet de requête sérialisable ;
- un schéma JSON simple ;
- un validateur de sortie structurée ;
- un registre d'outils ;
- un parseur de Tool Call ;
- des tests unitaires couvrant les cas valides et invalides.

### AI Engineering

L'apprenant doit pouvoir justifier :

- le choix d'une sortie structurée plutôt qu'un texte libre ;
- le découplage entre raisonnement modèle et exécution applicative ;
- l'usage de tests déterministes avant l'intégration avec un fournisseur réel ;
- les risques associés aux appels d'outils non contrôlés.

## Critères de réussite

Une solution est considérée correcte si :

- les structures de données sont explicites ;
- les sorties sont validées avant usage ;
- les outils sont appelés via un registre contrôlé ;
- les entrées invalides déclenchent des erreurs claires ;
- les tests passent sans accès réseau.
