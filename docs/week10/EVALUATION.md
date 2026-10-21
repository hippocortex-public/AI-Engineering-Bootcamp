# Protocole d’évaluation — Semaine 10

## Classification

Rapporter macro-F1 et accuracy argmax sur les douze tickets test après sélection verrouillée, avec matrice de confusion et ordre des classes. Rapporter séparément couverture et accuracy sélective au seuil choisi sur validation. Si aucun exemple n’est accepté, l’accuracy sélective vaut null. La baseline et le candidat adaptés sont évalués sur les mêmes ids.

Les probabilités ne sont pas calibrées et les exemples hors distribution sont des sondes, sans étiquette artificielle parmi les trois classes. Le rejet d’un vecteur nul ne couvre pas tous les textes étrangers au domaine. Les corpus sont fictifs et les scores très élevés ne représentent pas des garanties de production.

## Extraction

Comparer valeur et statut pour quatre champs sur quatre exemples : seize décisions chacun. Inspecter les preuves et leurs offsets. Distinguer absence et conflit; une valeur null n’établit pas à elle seule la bonne décision. Une mention de code HTTP ne prouve pas la présence d’une erreur actuelle.

## Résumé

Vérifier phrases source, ordre et budget. Le chevauchement multiensemble de tokens avec une référence est un proxy lexical, pas ROUGE ni une mesure de factualité. Ajouter une annotation d’unités d’information et d’omissions critiques avant un comparatif métier.

## Entités

Une correspondance requiert document, start, end et label identiques. Une mauvaise frontière ou un mauvais type produit un faux positif et un faux négatif. Les douze spans distribués concernent des noms connus du lexique; tester des noms inconnus et des formats difficiles avant de conclure au rappel général.

## Embeddings

Comparer TF-IDF et NCA sur le même index train et les mêmes requêtes test. La pertinence signifie même catégorie. Precision@3 et MRR@3 peuvent valoir 1 tandis que Recall@3 plafonne à 0,25 parce qu’il existe douze pertinents. Cette pertinence thématique ne garantit pas une réponse utile au ticket.

## Tests et mesures

Les tests de code vérifient les contrats et erreurs attendues. Ils ne remplacent aucune des mesures de tâche, qui elles-mêmes ne remplacent pas la revue métier. Conserver les cas, les versions, les empreintes et les limites avec les moyennes. Tout changement de sélection après lecture du test impose de reconnaître le nouveau protocole.
