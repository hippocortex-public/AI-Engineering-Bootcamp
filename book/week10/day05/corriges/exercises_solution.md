# Corrigé des exercices

## Exercice 1

Vocabulaire et IDF sont figés. Les coefficients et intercepts de la tête SGD peuvent changer. La baseline est clonée avant adaptation.

## Exercice 2

Non. transform applique un espace existant. Le mot peut être ignoré; une nouvelle représentation exige un nouvel entraînement compatible.

## Exercice 3

Appliquer la règle prévue : retenir le plus petit nombre d’epochs. La vitesse ou une autre contrainte préétablie pourrait aussi être un critère, sans sélection sur test.
