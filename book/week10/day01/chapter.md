# S10 J1 — Classification de textes et protocole sans fuite


## 1. Définir la tâche avant le modèle
Le projet classe des tickets en acces, deploiement ou performance. Le texte est l’entrée; la catégorie attendue est l’étiquette. Une classification mono-étiquette suppose qu’une seule catégorie suffit. Un ticket qui mêle release lente et jeton expiré peut contredire cette hypothèse. Documenter la règle d’annotation et prévoir une revue plutôt que présenter la classe comme une vérité universelle.

Le corpus contient 72 tickets fictifs : 36 train, 12 adaptation, 12 validation et 12 test. Les classes sont équilibrées dans chaque partition. Ces textes servent à entraîner et inspecter le protocole; ils ne représentent pas la diversité d’incidents réels. Les résultats faciles sur des formulations proches doivent rester visibles comme limite.

## 2. Empêcher les fuites
Les lignes possèdent id, group_id, split, label et text. Le validateur refuse les identifiants dupliqués, textes dupliqués normalisés et groupes répartis sur plusieurs splits. En pratique, grouper les messages d’un même incident, client ou conversation avant la répartition. Un simple tirage de lignes peut envoyer une reformulation du même problème dans le test.

Le vocabulaire et les IDF sont appris seulement sur train. Adaptation et validation utilisent transform, jamais fit. La validation sélectionne les réglages; le test sert à l’évaluation après sélection. Réexaminer le test pour choisir une nouvelle variante le transforme progressivement en jeu de développement.

## 3. Représenter et apprendre
TfidfVectorizer produit des unigrammes et bigrammes, normalise les accents et la casse, puis applique TF-IDF et une norme L2. La matrice creuse évite de stocker tous les zéros. Les bigrammes conservent un peu de contexte local, sans résoudre l’ordre global, les négations complexes ou les paraphrases éloignées.

SGDClassifier avec log_loss apprend réellement une tête linéaire par descente de gradient stochastique. Il ne s’agit ni d’un appel LLM ni de prédictions préfabriquées. Dans ce schéma multiclasses, scikit-learn combine des classifieurs one-vs-rest. La probabilité maximale n’est pas calibrée pour les exigences du métier.

## 4. Lire les métriques
La matrice de confusion utilise un ordre de classes explicite. Le macro-F1 donne le même poids à chaque classe; l’accuracy donne le même poids à chaque observation. Avec peu d’exemples et un corpus équilibré très simple, un score parfait ne prouve pas une fiabilité élevée sur de nouveaux tickets.

Le seuil d’acceptation est choisi sur validation parmi cinq valeurs fixées. La règle cherche la couverture maximale sous une accuracy sélective illustrative d’au moins 0,9. Si aucun seuil candidat ne satisfait la contrainte, la sélection est refusée plutôt que de conserver un seuil arbitraire. Coverage est la part de tickets acceptés; selective_accuracy porte uniquement sur ces tickets. En l’absence d’acceptation, ce dernier indicateur vaut null, pas un succès parfait.

## 5. Hors distribution
Le classifieur peut être confiant sur une phrase étrangère au domaine, notamment si quelques mots ordinaires sont connus du vocabulaire. Le garde de vecteur nul rejette seulement une entrée sans aucune caractéristique connue. Il ne constitue pas un détecteur fiable de hors-distribution.

Les exemples ood sont conservés sans inventer d’étiquette gold parmi les trois catégories. Ils illustrent le comportement du modèle et ses limites. Une exploitation réelle demanderait des négatifs représentatifs, une calibration, un contrôle des changements de distribution et une politique de revue.

## À retenir
L’apprentissage commence par le contrat de tâche et la séparation des données. Un bon score n’efface ni les ambiguïtés d’étiquette ni la faiblesse du corpus.
