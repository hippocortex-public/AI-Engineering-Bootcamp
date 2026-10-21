# S9 J2 — Embeddings, similarité et compatibilité


## 1. Représenter un texte par des nombres
Un embedding transforme une entrée en un vecteur. Son intérêt dépend de ce que sa géométrie encode. Deux textes proches selon le vecteur peuvent partager des mots, un thème, une intention ou seulement une collision de représentation. La dimension n’est pas un score de qualité et un cosinus élevé ne devient pas une probabilité de réponse correcte.

Le lab obligatoire implémente HashEmbedding : une projection signée des comptes de mots vers 128 dimensions. C’est une baseline lexicale calculée réellement, sans valeurs préfabriquées. Elle n’apprend rien et ne comprend pas les synonymes. La nommer « recherche sémantique neuronale » serait incorrect.

## 2. Projection signée et normalisation
La fonction tokens normalise casse et accents, retire une liste fixe de mots courants et conserve des termes alphanumériques. Chaque terme est associé par SHA-256 à une case et à un signe; son compte est ajouté à la case. La norme L2 sert ensuite à normaliser le vecteur. Un texte sans termes utiles produit le vecteur nul.

SHA-256 garantit ici une projection déterministe entre processus, contrairement à hash() de Python dont le comportement n’est pas destiné à définir un index stable. Cela ne supprime pas les collisions : plusieurs termes peuvent atteindre la même dimension et leurs signes peuvent se compenser. Une faible dimension rend ce problème plus visible.

## 3. Similarité cosinus
Le cosinus est le produit scalaire divisé par le produit des normes. Pour deux vecteurs non nuls normalisés, il coïncide avec le produit scalaire. Le lab retourne zéro lorsqu’un vecteur est nul et refuse les dimensions différentes ou les valeurs non finies.

« Kafka paiement » et « paiement Kafka » possèdent le même sac de mots. Leur cosinus vaut environ un, mais l’ordre des mots a disparu. Une négation peut modifier fortement le sens sans changer suffisamment la représentation. C’est une limite du modèle lexical, pas un bug du calcul de cosinus.

## 4. Passer à un modèle appris
Un bi-encoder neuronal calcule séparément les vecteurs de requête et de document. Certains modèles utilisent des prompts ou tâches distincts pour ces deux côtés. L’adaptateur optionnel applique encode_query et encode_document et normalise leurs sorties. Il exige des poids déjà présents localement; aucun téléchargement n’est déclenché par le code.

Choisir un modèle pour sa langue, sa tâche et sa contrainte d’exploitation. Tester les paraphrases, identifiants techniques et cas négatifs. La requête q8 emploie une paraphrase éloignée du vocabulaire du corpus : elle expose une faiblesse de la baseline plutôt que de masquer les échecs derrière des questions trop faciles. Les modèles neuronaux et leur qualité ne sont pas validés dans cet environnement.

## 5. Compatibilité d’index
Le store conserve une empreinte du modèle et sa dimension. Ouvrir une base hashbow en 64 dimensions avec un encodeur de 128 dimensions est refusé. Changer de modèle avec la même dimension doit aussi être refusé : la signification des axes peut être différente. Une comparaison de vecteurs de longueur égale ne suffit pas.

Versionner aussi le tokenizer, les prompts d’encodage et la normalisation. L’adaptateur neuronal calcule une empreinte des artefacts locaux. Pour une migration, créer un index distinct, le reconstruire et comparer les résultats avant bascule. Mélanger progressivement deux espaces dans une même collection rend les scores incohérents.

## 6. Expérience du jour
Comparer vecteurs identiques, vecteur nul, ordre des mots inversé et dimension très faible. Distinguer le résultat du calcul et son interprétation métier. Le cours de S1 expliquait le concept; ici l’enjeu est son contrat d’indexation et la migration de ses artefacts.

## À retenir
La géométrie d’un embedding dépend de sa construction. Un espace compatible et une expérience de pertinence comptent davantage qu’une grande dimension ou un score isolé.
