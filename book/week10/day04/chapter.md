# S10 J4 — NER, offsets et masquage contrôlé


## 1. NER et extraction structurée
La reconnaissance d’entités nommées repère des occurrences typées dans un texte. L’extraction J2 agrège des occurrences vers un schéma métier avec valeurs normalisées et ambiguïtés. Plusieurs entités SERVICE peuvent être reconnues sans savoir laquelle est responsable de l’incident. Les tâches se complètent mais ne se substituent pas l’une à l’autre.

Le lab utilise un lexique de services et technologies ainsi qu’une regex email. Il n’entraîne pas de modèle NER neuronal. Le choix est explicite pour concentrer l’expérience obligatoire sur frontières de spans, collisions et évaluation. Une méthode apprise demanderait annotations, entraînement et comparaison sur des entités inconnues.

## 2. Contrat de span
Chaque entité contient start, end, text et label. Les indices sont des positions de caractères Python dans le texte original, avec end exclusif. Les accents et la casse originale restent conservés, même si le motif utilise une recherche insensible à la casse. Une réponse d’API ou une interface Java doit préciser l’unité : les offsets UTF-16 ne sont pas toujours les indices Unicode Python.

L’égalité text == source[start:end] est nécessaire. Le typage et la frontière exacte comptent aussi : reconnaître seulement Paiement au lieu de Paiement API ne réussit pas le protocole strict. Les quatre exemples sont annotés explicitement sans appeler le détecteur pour fabriquer leur gold.

## 3. Chevauchements et règles
Les candidats sont triés par longueur décroissante et une sélection évite les chevauchements. Les entités retenues sont remises dans l’ordre source. Le lexique protège les limites de mots pour éviter de reconnaître prod à l’intérieur de production ou Redis dans une chaîne plus longue.

Cette politique privilégie la simplicité et un span long. Elle ne gère pas des entités imbriquées. D’autres corpus pourraient avoir besoin de plusieurs couches d’annotation, d’un schéma BIO par token ou d’un modèle spaCy/Transformer. L’évolution du schéma fait partie de la tâche, pas seulement du choix de bibliothèque.

## 4. Évaluation stricte
Une correspondance exige même document, début, fin et type. Un mauvais type compte comme une prédiction incorrecte et laisse une entité gold manquante. Les métriques précision, rappel et F1 sont calculées sur les ensembles de spans. Les cas sans prédiction ne reçoivent pas automatiquement un score parfait.

Le lexique réussit les noms connus du petit corpus, ce qui ne mesure pas la généralisation. Un nouveau service inconnu peut être totalement omis. Ajouter au jeu réservé des noms absents du lexique, des variantes et des mots ordinaires ressemblant à des entités. Ne pas seulement mesurer les formes qui ont servi à écrire les règles.

## 5. Masquage
mask_entities remplace les spans depuis la fin vers le début afin que les premières positions ne soient pas décalées pendant les remplacements. Il vérifie bornes, texte et absence de chevauchement avant de modifier le résultat. Les labels remplacent les mentions reconnues; ils ne produisent pas un identifiant de pseudonyme stable.

Ce masquage est partiel. Une personne, un secret ou une adresse écrite autrement peut ne pas être reconnue. Il n’établit aucune anonymisation juridique ou technique générale. Les offsets du texte original ne doivent pas être réutilisés comme s’ils pointaient dans le texte masqué.

## 6. Lecture des négations
« Ne pas utiliser Redis » contient bien une mention de technologie Redis. La NER ne signifie pas que Redis est utilisé, responsable ou autorisé. Pour produire cette conclusion, il faudrait une analyse de relation et de polarité. La reconnaissance d’une chaîne ne doit pas déclencher une action métier.

## À retenir
Les frontières, types et conventions d’offsets font partie du contrat. Un bon F1 sur des noms connus ne prouve pas un masquage exhaustif des données sensibles.
