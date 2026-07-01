# Corrigé — Questions d’entretien

## Objectif

Ce fichier fournit une grille de correction pour les questions d’entretien du jour 03.

## Réponses attendues

### Question 1 — Clarifier le problème

Une bonne réponse doit montrer que l’apprenant sait :

- reformuler le besoin métier ou technique ;
- identifier les contraintes ;
- distinguer les hypothèses des faits ;
- proposer une solution vérifiable.

### Question 2 — Raisonner comme un AI Engineer

Une réponse solide inclut généralement :

- une description du pipeline de données ou d’inférence ;
- une stratégie d’évaluation ;
- une gestion explicite des erreurs ;
- une réflexion sur les coûts, la latence et la maintenabilité.

### Question 3 — Qualité de production

Points attendus :

- tests unitaires ou tests d’intégration ;
- logs utiles et non verbeux ;
- configuration séparée du code ;
- reproductibilité de l’environnement ;
- documentation minimale pour relancer le travail.

## Exemple de réponse courte

> Je commencerais par définir l’entrée, la sortie et le critère de succès.  
> Ensuite, je construirais une version minimale mesurable, avec tests et logs.  
> Enfin, je comparerais la sortie obtenue à une baseline avant d’optimiser.

## Grille d’évaluation

| Niveau | Critères |
|---|---|
| Insuffisant | Réponse vague, pas de contraintes, pas de validation. |
| Correct | Solution compréhensible, mais validation partielle. |
| Bon | Raisonnement structuré, erreurs anticipées, solution testable. |
| Excellent | Vision production, observabilité, compromis explicités. |

## Notes formateur

Adapter les réponses aux questions exactes de `interview.md` si elles diffèrent.  
Ce fichier doit rester dans `corriges/`.
