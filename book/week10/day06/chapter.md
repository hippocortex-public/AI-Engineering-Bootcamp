# S10 J6 — Embeddings spécialisés par apprentissage métrique


## 1. De la représentation générale à une tâche
S9 présentait espaces vectoriels et compatibilité d’index. Ce jour apprend une transformation à partir d’étiquettes : les tickets d’une même catégorie doivent devenir utiles comme voisins. Il ne réécrit pas le moteur de retrieval de S9 et ne présente pas un index supervisé comme une compréhension sémantique générale.

Le point de départ est le TF-IDF appris seulement sur train. Neighborhood Components Analysis apprend une projection linéaire supervisée, optimisée pour une décision par voisinage. Le module utilise une représentation dense du tout petit corpus; ce choix ne serait pas adapté sans mesure à un très grand vocabulaire.

## 2. Apprendre sans voir les questions test
La projection reçoit les 36 tickets train et leurs étiquettes. Les douze tickets test sont des requêtes après entraînement; l’index de voisins contient uniquement les tickets train. Le test n’est pas un index dans lequel on retrouverait la question elle-même.

La dimension cible est huit et la graine est fixée. Le rapport garde le nombre d’itérations et les éventuels avertissements d’optimisation. Le code borne les threads de calcul pour limiter la variabilité de cette petite expérience; il ne promet pas des poids identiques sur toutes les versions matérielles et logicielles.

## 3. Ce que la projection peut apprendre
NCA cherche une géométrie utile aux catégories connues. Elle peut rapprocher des tickets de déploiement et éloigner des refus d’accès, même si certains mots se recouvrent. Elle peut aussi écraser des distinctions importantes à l’intérieur d’une catégorie : deux incidents performance n’ont pas forcément le même remède.

La pertinence du rapport est donc un proxy « même catégorie », pas une annotation humaine de réponse à une question. Un meilleur classement par thème ne prouve pas qu’un ticket explique le problème de l’autre. Distinguer compression, classification par voisinage et recherche de connaissance réellement pertinente.

## 4. Protocole de comparaison
Les deux modes utilisent le même index train et les mêmes requêtes test. On calcule le cosinus après normalisation dans chaque espace. Le top trois est départagé de manière stable par identifiant lorsque les scores sont égaux. Les requêtes sont ensuite évaluées selon la catégorie des voisins.

Precision@3 mesure la part des trois voisins du bon thème. MRR@3 mesure le rang du premier. Recall@3 divise par tous les documents train du thème : douze par catégorie. Son maximum dans ce corpus est donc 3/12=0,25, même avec trois voisins corrects. Ne pas interpréter ce plafond comme un défaut du calcul.

## 5. Lire un gain sans l’exagérer
Dans l’environnement de référence, l’espace passe de 441 dimensions TF-IDF à huit dimensions NCA. La précision thématique moyenne des trois premiers voisins augmente dans cette expérience. Le premier pertinent était déjà bien placé, donc MRR peut rester inchangé. Le rapport conserve les cas et les deux modes au lieu d’un seul chiffre favorable.

Un corpus différent, d’autres catégories ou une distribution modifiée peuvent inverser ce résultat. Pour une vraie spécialisation sémantique, annoter des paires pertinentes et non pertinentes, choisir une méthode adaptée et réserver un test hors des templates de développement. Le module n’entraîne pas d’encodeur neuronal ni de Sentence Transformer.

## 6. Versionner l’espace
La projection dépend du vocabulaire, des IDF, des composants appris et des données. Le rapport conserve une empreinte des caractéristiques et du train. Changer l’un de ces éléments demande de reconstruire les vecteurs de l’index; des dimensions égales ne suffisent pas à assurer la compatibilité.

## À retenir
Un embedding spécialisé optimise une tâche définie. Une bonne géométrie pour les catégories n’est pas automatiquement une bonne géométrie pour toutes les questions métier.
