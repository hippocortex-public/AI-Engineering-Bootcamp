# S10 J7 — Projet NLP intégré et revue des erreurs


## 1. Ce que reçoit le projet
Une entrée textuelle produit une classe ou une demande de revue, quatre champs extraits avec preuves, un résumé extractif et des spans d’entités. Le résultat ne publie rien et ne modifie aucun compte. Il prépare une analyse que le système applicatif pourrait consommer après validation de ses propres droits et règles.

Les blocs ne sont pas tous appris. La classification et la projection NCA sont entraînées réellement; la tête est adaptée sur un corpus distinct. L’extraction et la NER utilisent des règles, le résumé une centralité TF-IDF. Les désigner séparément permet d’expliquer les erreurs et de choisir une amélioration ciblée.

## 2. Contrat de revue
requires_review vaut vrai lorsque la classification s’abstient, que le ticket_id n’est pas présent ou qu’un champ est ambigu. Un champ optionnel absent ne provoque pas automatiquement une revue. Cette règle est illustrative; elle ne devient pas une autorisation d’agir sur un environnement de production.

Les textes d’exemple ne forment pas un jeu complet de routing. Le classifieur a été entraîné sur des tickets courts; les exemples intégrés sont plus longs et multi-sujets. Inspecter ses sorties au lieu de supposer que les bons résultats de test s’appliquent inchangés à ces nouveaux formats.

## 3. Trois familles de preuve
Les tests logiciels vérifient invariants et cas limites : partitions séparées, offsets, unités, conflits, budget, masquage et rechargement d’artefact. Les métriques de tâche décrivent un comportement sur un corpus : macro-F1, matrice, spans exacts, recouvrement lexical et voisinage thématique. La revue métier détermine l’utilité et les conséquences d’une erreur.

Ces preuves ne sont pas interchangeables. Une suite de tests ne prouve pas la qualité sur tous les tickets; un F1 parfait sur douze exemples ne prouve pas l’absence de bug. Une référence de résumé très proche peut masquer une condition omise. La décision doit garder les trois niveaux visibles.

## 4. Résultats de référence
Dans l’environnement validé, baseline et tête adaptée ont le même F1 de test sur le corpus facile. Les poids changent réellement, mais l’expérience ne démontre pas de gain de classification. Les champs et entités connus sont correctement reconnus sur les quatre exemples annotés, avec une ambiguïté explicitement traitée.

La projection NCA améliore la précision de voisinage par catégorie dans ce petit échantillon. Elle ne mesure pas une pertinence sémantique humaine générale. Les rapports gardent les cas, les ids et les avertissements pour permettre une inspection au-delà des moyennes.

## 5. Artefacts et reproduction
La commande de rapports réentraîne les composants avec la graine fixée, applique les choix de validation puis écrit rapports et classifieurs JSON. Elle enregistre les versions NumPy/scikit-learn/SciPy et les empreintes des données. Le module S10 possède ses dépendances épinglées sans remplacer le pyproject du dépôt.

Les artefacts JSON contiennent les tableaux nécessaires à l’inférence de classification, sans pickle. Leur hash est un contrôle de cohérence local, pas une signature. Pour une livraison réelle, ajouter un stockage/provenance contrôlés et une politique de versions de modèle, données et protocole.

## 6. Prochaine expérience utile
Si les tickets sont nouveaux et ambigus, collecter une annotation représentative avant de choisir un plus grand modèle. Si les noms inconnus manquent, évaluer une NER apprise. Si les formulations courtes ne suffisent pas, analyser le traitement de texte long et ses segments. Si une adaptation LoRA est justifiée, exécuter le lab optionnel avec artefacts locaux et un protocole réservé.

Le projet S11 pourra assembler ces capacités avec API, agents et gouvernance. Cette archive fournit un module autonome et des contrats documentés; elle ne prétend pas avoir branché votre application existante ni déployé un service.

## À retenir
Un projet NLP exploitable sait expliquer ce qu’il apprend, ce qu’il règle, ce qu’il mesure et quand il demande une revue.
