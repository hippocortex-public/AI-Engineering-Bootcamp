# S9 J3 — Vector store, persistance et filtres


## 1. Un vecteur seul ne suffit pas
Un système documentaire doit stocker texte, source, version et droits avec la représentation vectorielle. Une liste de nombres sans provenance ne permet ni citation ni suppression cohérente. Un vector store définit aussi une stratégie d’ingestion, de filtrage, d’évolution et de récupération après panne.

Le parcours obligatoire utilise SQLite pour la persistance et Python pour un scan exact des vecteurs autorisés. SQLite n’est pas configuré comme une base vectorielle avec index ANN. Ce choix rend la mécanique visible et testable hors ligne sur quelques dizaines de passages. L’extension pgvector est étudiée dans un lab optionnel séparé, sans prétendre avoir été exécutée.

## 2. Contrat de la collection
La table documents garde le document courant par couple tenant/doc_id. La table chunks garde les projections et leurs vecteurs. La table metadata conserve l’empreinte de l’encodeur. La même version documentaire avec un autre contenu est refusée; une version inférieure à la courante l’est aussi.

L’ingestion prépare chunks et vecteurs, puis supprime les anciennes projections et écrit les nouvelles dans une transaction. Refaire le même contenu peut reconstruire le découpage; cela ne crée pas de doublons. Un échec d’encodage arrive avant la mutation. Un échec SQL dans la transaction doit laisser l’ancienne projection exploitable.

## 3. Filtrer avant de classer
scoped_rows exécute une requête SQL WHERE tenant=? avant tout calcul de score. La sélection top-k n’utilise donc que le périmètre voulu. Un document team-b peut contenir exactement la requête et rester absent des résultats team-a. Filtrer après un top-k global peut éliminer tous les candidats utiles et gaspiller la recherche sur un autre périmètre.

Le paramètre tenant suppose une décision d’autorisation déjà prise côté service. Le CLI de laboratoire permet de choisir le tenant pour tester les cas; il ne fournit pas d’authentification. Un service réel dériverait le périmètre de l’identité et des ressources autorisées, avec éventuellement des droits plus fins que le seul tenant.

## 4. Recherche exacte et ANN
Le scan exact calcule toutes les similarités dans le périmètre, puis trie. Il sert de baseline. Un index approximatif réduit souvent le coût de recherche mais introduit un compromis entre rappel, latence, mémoire et mise à jour. Le mesurer sur des requêtes représentatives plutôt que promettre le même résultat à partir du seul nom HNSW.

Avec des filtres et un index ANN, la mécanique d’exécution demande une attention particulière : le nombre de candidats réellement éligibles peut être plus petit que prévu. Le dossier optionnel présente pgvector, son opérateur de distance cosinus et une requête paramétrée. L’étude des scans itératifs et des paramètres d’index doit être faite sur l’installation réelle.

## 5. Cycle de vie
Une nouvelle version remplace les chunks de la précédente. Une citation contenant un ancien chunk_id devient invalide. delete_document supprime document, chunks et mémoires référencées. Cette opération ne garantit pas l’effacement des anciennes sauvegardes ou copies externes; elle définit le comportement observable du store local.

Le modèle est une autre dimension de version. Changer son empreinte exige un index distinct et une reconstruction. Une migration propre peut conserver ancien et nouvel index le temps de comparer les résultats puis basculer un pointeur de service. Le lab ne fournit pas cet opérateur de bascule ni un cluster distribué.

## 6. Preuve du jour
Écrire dans une base fichier, fermer puis rouvrir. Vérifier les mêmes identifiants classés. Ajouter une version 2 et vérifier l’absence des anciens passages. Faire correspondre la suppression à l’absence de résultats et à l’invalidation d’une citation. Ces preuves sont plus utiles que la seule réussite d’un INSERT.

## À retenir
La qualité d’un store vectoriel dépend autant de ses filtres, versions et suppressions que du calcul de distance. Le moteur local prouve ces contrats sur un processus, pas une capacité distribuée.
