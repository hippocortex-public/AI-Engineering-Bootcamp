# Revue pédagogique

## Acquis à vérifier

- Séparer erreurs transitoires et erreurs permanentes.
- Mettre en œuvre une reprise bornée et une quarantaine observable.
- Décrire l’outbox et la fenêtre de panne d’un effet externe.

## Erreurs fréquentes

Confondre réception et achèvement; assimiler un exemple simulé à une évaluation de modèle; déduire une garantie distribuée d’une transaction locale. Pour ce jour, vérifier en particulier : L’outbox conserve l’intention et la progression locale. Elle ne prouve pas que le destinataire n’a rien reçu. Réutiliser une clé stable chez le destinataire ou réconcilier; sinon doublon possible.

## Barème indicatif sur 10

- 3 points : explication des concepts avec le scénario du support.
- 3 points : reproduction du lab et analyse de sa sortie.
- 2 points : réponses aux exercices, sans confusion sur les garanties.
- 2 points : challenge argumenté et limite opérationnelle identifiée.

Le parcours essentiel peut être validé sans le challenge. Toute publication sans validation bloque la validation du projet intégré, quel que soit le score.
