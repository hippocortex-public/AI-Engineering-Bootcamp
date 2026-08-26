# Review formateur — S4 J3

## Intention pédagogique

Cette journée transforme la notion de tool en composant de framework. Les apprenants doivent sortir du simple “function calling” et raisonner comme des ingénieurs backend : contrats, permissions, erreurs, traces et frontières d’exécution.

## Points à vérifier

- L’apprenant distingue bien tool public et handler interne.
- Il comprend que la validation serveur reste obligatoire.
- Il n’expose pas les outils sensibles par défaut.
- Il utilise `blocked` pour une politique refusée et `failed` pour une erreur.
- Il produit des tests sur les cas négatifs, pas seulement sur les cas heureux.
- Il ne mélange pas tool registry et memory layer.

## Démonstration recommandée

1. Lister les tools sans `include_sensitive`.
2. Appeler `add_numbers` correctement.
3. Appeler `add_numbers` avec un champ extra.
4. Appeler `search_policy` sans scope.
5. Appeler `create_ticket` avec scope mais sans approbation.
6. Rejouer `create_ticket` avec scope et approbation.
7. Lire la trace produite.

## Questions de relance

- Que se passe-t-il si un modèle hallucine un nom de tool ?
- Où placerais-tu les retries ?
- Comment limites-tu l’exposition des tools selon le rôle de l’agent ?
- Quelles traces seraient nécessaires en production ?
- Comment éviter qu’un outil devienne un accès non contrôlé à la base de données ?

## Critères de validation

Une solution est acceptable si elle :

- possède un registre central ;
- valide les arguments avant exécution ;
- protège les outils sensibles ;
- retourne des résultats normalisés ;
- capture les erreurs handler ;
- reste testable sans fournisseur externe.
