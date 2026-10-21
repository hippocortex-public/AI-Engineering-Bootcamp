# S9 J1 — Chunking, provenance et cycle documentaire


## 1. Le passage devient l’unité de recherche
Un système de connaissances ne retrouve pas seulement des documents : il prépare des passages assez précis pour répondre et assez complets pour garder leur sens. Découper trop finement isole une phrase de sa condition; découper trop largement dilue le signal et consomme du contexte. Le bon découpage dépend de la structure du corpus et des questions attendues.

Le fil rouge utilise huit documents fictifs de backend et DevOps. Sept appartiennent à team-a; un document voisin appartient à team-b. Les procédures et valeurs sont des conventions du lab. L’objectif est de construire la chaîne documentaire et ses contrôles, sans faire passer ces notes pour une documentation d’un système bancaire réel.

## 2. Définir un contrat documentaire
Chaque document porte doc_id, tenant, version, title, source et text. Le tenant représente un périmètre déjà autorisé par le serveur dans une architecture réelle. Il ne doit pas venir d’un choix libre d’un client qui obtiendrait ainsi les droits d’un voisin. La version est un entier positif; une modification du contenu exige une nouvelle version.

Le document constitue la source de vérité. Les chunks et vecteurs sont des projections reconstruites. Une suppression de source doit aussi retirer ses passages de l’index. Un index oublié après une suppression peut continuer à exposer une ancienne information même si le fichier d’origine a disparu.

## 3. Algorithme local
chunk_document identifie les paragraphes puis crée des fenêtres de mots séparés par des espaces. Une fenêtre longue de max_words avance de max_words−overlap jusqu’à la fin du paragraphe. La garde overlap < max_words garantit la progression. Un paragraphe court produit un seul chunk et ne doit pas créer de doublon final.

Les mots de découpage ne sont pas les tokens d’un modèle. Les offsets start/end sont des indices de caractères Python dans le texte Unicode original. La propriété à vérifier est source[start:end] == chunk.text. La normalisation utilisée plus tard pour rechercher n’altère pas le texte cité ni ses positions.

## 4. Taille, chevauchement et structure
Le chevauchement protège un peu les relations autour d’une frontière, mais augmente le nombre de passages et la redondance. Il ne garantit pas qu’une condition éloignée reste présente. Mesurer les questions qui échouent avant de choisir une valeur universelle. Des listes, tableaux ou blocs de code peuvent demander un découpage différent de la prose.

Le chunker fourni garde aussi les titres isolés comme petits chunks. Cette simplicité révèle un bruit utile à observer : un titre peut être très bien classé sans fournir la réponse. Le mode extractif final ignore les chunks constitués d’un paragraphe de titre. Une amélioration serait de rattacher le titre au paragraphe tout en gardant des offsets exacts et un budget explicite.

## 5. Identité et évolution
L’identifiant d’un chunk dérive de tenant, doc_id, version, offsets et texte. Refaire le même découpage produit les mêmes identifiants. Modifier le chevauchement ou la version peut produire un autre ensemble. Le titre et la source restent dans les métadonnées; une modification du document avec la même version est refusée par le store.

L’ingestion prépare les vecteurs avant de remplacer l’ensemble des chunks dans une transaction. Si l’encodage ou l’écriture échoue, les passages précédents restent disponibles. Ce remplacement atomique concerne un document dans le processus SQLite; il ne prétend pas synchroniser un stockage documentaire externe et un cluster vectoriel.

## 6. Preuve du jour
Vérifier les offsets sur un document accentué, un paragraphe long et un texte sans ligne vide. Compter le surplus créé par overlap. Conserver un exemple où une question exige deux passages afin de montrer la limite d’un découpage purement mécanique. Le chunking ne résout ni pertinence ni autorisation : il prépare leur unité de travail.

## À retenir
Un chunk utile a une taille maîtrisée, une provenance vérifiable et un cycle de vie relié à la source. Une chaîne de recherche ne peut pas réparer une condition perdue lors du découpage.
