# S9 J4 — Hybrid Search : BM25 et fusion des rangs


## 1. Pourquoi deux canaux ?
Une recherche lexicale valorise les termes présents, notamment codes d’erreur, identifiants et noms de composants. Un encodeur neuronal peut retrouver des paraphrases. La recherche hybride vise une complémentarité, pas un remplacement automatique du lexical. Dans ce lab, les deux canaux restent lexicaux : BM25 et projection hashbow. Leur fusion démontre le protocole, sans prouver un gain sémantique.

La requête q8 utilise un vocabulaire éloigné des passages pertinents. Elle rend visible le défaut commun des deux représentations. Si deux canaux partagent la même faiblesse, fusionner leurs rangs ne crée pas l’information manquante.

## 2. BM25 local
Le score dépend de la fréquence d’un terme dans un passage, de sa rareté dans le corpus et de la longueur du passage. La saturation évite qu’une répétition illimitée du même mot augmente linéairement le score. La normalisation de longueur évite de favoriser systématiquement les grands passages.

Le module utilise k1=1,2, b=0,75 et une formule IDF positive explicite dans le code. Les termes de la requête sont dédupliqués. La tokenisation est celle du lab; elle n’a pas de stemming ni de compréhension des synonymes. Les paramètres sont une baseline, pas une recommandation universelle.

## 3. Des scores non comparables
Un score BM25 n’a pas la même distribution qu’un cosinus. Les additionner sans calibration attribue une importance arbitraire aux deux systèmes. La fusion RRF utilise les rangs : pour un candidat, additionner 1/(c + rang) dans les listes où il apparaît. Les rangs commencent à 1 et c vaut 60 dans le lab.

Un candidat absent d’une liste ne reçoit aucune contribution de celle-ci. Un même chunk ne peut pas apparaître deux fois dans une seule liste. La fusion conserve les métadonnées et trie les égalités de manière déterministe par identifiant. La constante amortit les écarts de rang; elle n’est ni un seuil de confiance ni une probabilité.

## 4. Profondeur de candidats
candidate_k borne le nombre de passages de chaque canal avant fusion. top_k borne le nombre final retourné. Si un passage manque dans toutes les listes de candidats, la fusion et le reranker ne pourront pas le récupérer. Évaluer le rappel à une profondeur suffisamment grande avant d’optimiser seulement le premier résultat.

Les métriques de la semaine sont calculées au niveau document. Plusieurs chunks d’une même source sont dédupliqués en gardant la première occurrence avant Recall@k, MRR@k et nDCG@k. Sans cette convention, un document possédant de nombreux chunks pourrait occuper tous les rangs et masquer l’absence d’autres sources.

## 5. Filtrage et protocole
Les deux canaux voient les mêmes passages autorisés. BM25 calcule ses fréquences documentaires sur ce sous-corpus. Le vecteur de requête est comparé uniquement aux vecteurs de ce périmètre. Le corpus, la tokenisation et la dimension sont tracés dans les rapports. Un changement du corpus demande une nouvelle mesure, comme les changements de protocole de S8.

Le petit jeu de développement ne doit pas devenir une preuve de production. Les questions proches du texte peuvent être faciles pour toutes les variantes. Examiner q8 et ajouter de nouveaux cas annotés sans transformer silencieusement les qrels pour améliorer le résultat.

## 6. Expérience du jour
Construire deux listes simples, calculer RRF à la main et vérifier le résultat du code. Comparer lexical, vector et hybrid sur toutes les requêtes. Une égalité de performance est un résultat acceptable; le cours ne doit pas annoncer une supériorité qui n’est pas observée.

## À retenir
L’hybridation combine des preuves de retrieval avec un protocole explicite. Elle ne rend pas compatibles deux espaces par magie et ne répare pas un candidat absent des listes.
