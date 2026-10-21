# S10 J2 — Extraction structurée, valeurs et ambiguïtés


## 1. Extraire n’est pas simplement repérer
Un ticket peut mentionner plusieurs codes HTTP ou deux mesures de latence. L’extraction doit produire un objet cohérent avec le contrat attendu, pas seulement toutes les chaînes ressemblant à une valeur. Le lab extrait ticket_id, environment, http_status et duration_ms. Ces champs sont ensuite utilisables par un système, mais aucune action n’est déclenchée.

La méthode obligatoire est une baseline par expressions régulières et normalisation contrôlée. Elle n’est pas un modèle appris. Sur un format stable, cette simplicité peut suffire; sur des formulations variées ou des relations complexes, elle atteint vite ses limites.

## 2. Valeur et preuve
Chaque champ porte status, value et evidence. Une preuve conserve start, end, text et valeur normalisée. La propriété source[start:end] == evidence.text permet d’inspecter ce qui a déclenché l’extraction. Le texte original n’est pas remplacé par une version nettoyée avant de calculer les positions.

Un code HTTP est un entier entre 100 et 599 selon le motif reconnu. Une durée est représentée par une chaîne décimale en millisecondes. Le nombre 1,5 s devient 1500 sans dépendre d’un flottant binaire. L’environnement production est normalisé en prod; les autres valeurs autorisées restent explicites.

## 3. Manquant et ambigu
Aucune occurrence produit missing et value=null. Plusieurs occurrences portant la même valeur peuvent rester present avec plusieurs preuves. Deux valeurs distinctes produisent ambiguous et value=null. Les preuves sont conservées au lieu de sélectionner arbitrairement la première.

Le cas e4 compare HTTP 401 et HTTP 503 et mentionne deux latences. Le contrat ne sait pas quelle occurrence est la bonne mesure cible; il la marque ambiguë. Null ne suffit donc pas pour évaluer le comportement : il faut comparer aussi le statut. Les rapports comptent séparément valeurs et statuts corrects.

## 4. Ce que le motif ne comprend pas
Trouver HTTP 500 dans « aucun HTTP 500 observé » reconnaît une mention, pas une affirmation d’erreur présente. Le champ du lab représente le code cité, sans prétendre inférer une causalité ni un état d’alerte. Une extraction métier d’incident actuel demanderait un contrat plus riche pour la négation, la chronologie et les comparaisons.

Le motif de durée attend latence ou durée, une quantité et une unité s/ms. Une autre écriture peut ne pas être reconnue. Ajouter des formats à partir de cas annotés; ne pas faire évoluer la regex pour réussir un seul exemple sans vérifier les anciens cas.

## 5. Validation d’un objet extrait
Une extraction générative via Structured Outputs pourrait contraindre la forme JSON, mais la forme ne prouverait pas l’appui textuel des valeurs. Conserver preuves, unités et politique d’ambiguïté même si la méthode change. Le lab n’exécute pas cette variante générative.

L’application intégrée demande une revue si l’identifiant de ticket manque, si la classification s’abstient ou si un champ est ambigu. L’absence d’un code HTTP n’est pas forcément un défaut : tous les incidents n’en ont pas. Les champs obligatoires et optionnels relèvent du besoin métier.

## 6. Évaluer
Les quatre textes d’exemple possèdent une annotation de valeur et de statut par champ. Cela représente seize décisions de champ, avec absences et conflits. Un résultat parfait sur ces formats ne mesure pas la robustesse à la langue naturelle générale. Ajouter erreurs d’écriture, unités, négations et chronologie avant d’utiliser la sortie dans un traitement réel.

## À retenir
Une extraction exploitable conserve le lien au texte et expose l’incertitude du contrat. Une valeur manquante et une valeur contradictoire demandent des traitements différents.
