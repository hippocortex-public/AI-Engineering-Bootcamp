# S9 J5 — Reranking, diversité et budget de contexte


## 1. Retrouver puis reclasser
Le retriever sélectionne rapidement des candidats; le reranker les examine avec la requête. Cette séparation permet un traitement plus coûteux sur un petit ensemble. Un reranker ne recherche pas dans tout le corpus et ne peut pas découvrir un passage absent. Une amélioration du premier rang ne compense pas un rappel initial trop faible.

Le module obligatoire utilise une heuristique réelle et transparente : couverture des termes de la requête dans le texte, avec un petit bonus de couverture dans le titre. Elle calcule une fonction de la paire, mais n’est pas un CrossEncoder neuronal. L’adaptateur optionnel fournit une interface pour un modèle appris local non exécuté ici.

## 2. Interpréter le score
term_coverage est la proportion de termes de requête présents dans le passage. Le score ajoute 0,1 fois la couverture du titre. Un score élevé peut simplement révéler des mots communs; il ne démontre pas que le passage répond correctement. Le score du retriever est conservé sous retrieval_score afin de ne pas confondre les deux étapes.

Un CrossEncoder appris traite conjointement la requête et le candidat. Sa sortie peut être un logit, un score de pertinence ou une autre valeur selon le modèle. Elle ne devient pas automatiquement une probabilité de vérité. La calibration et l’évaluation restent nécessaires, y compris quand le modèle est préentraîné pour le reranking.

## 3. Sélectionner sous contrainte
context_pack ajoute les passages entiers tant que le budget de mots le permet. Il peut sauter un grand passage et conserver un passage plus court suivant. Le budget est en mots séparés par espaces, pas en tokens LLM. Il n’inclut pas le coût complet d’un prompt de génération; une intégration réelle doit compter instructions, question, wrappers et réserve de sortie.

Ne pas tronquer silencieusement un passage cité en conservant ses anciens offsets. Le mode local garde les extraits entiers et vérifiables. Si le budget ne contient aucun candidat suffisamment étayé, la réponse s’abstient. Une absence de preuve vaut mieux qu’une citation fabriquée.

## 4. Redondance et diversité
Plusieurs chunks d’un même document peuvent être pertinents mais redondants. Un chevauchement important amplifie ce phénomène. Le moteur de base n’implémente ni MMR ni déduplication sémantique; le challenge propose un packing limité à un passage par document pour étudier le compromis de diversité.

Une réponse peut aussi exiger deux passages complémentaires du même document. Imposer une seule source par document partout ferait perdre cette complémentarité. Mesurer le besoin avant d’appliquer une règle de diversité uniforme. Le projet conserve tous les identifiants de citations pour permettre cette inspection.

## 5. Un seuil d’abstention explicite
Le mode extractif exige une couverture minimale de 0,6, retire les chunks de titre isolés et applique le budget. Ce seuil est pédagogique et lexical. Il peut refuser une excellente paraphrase sans mots communs ou accepter un texte trompeur qui répète la requête. Il ne doit pas être présenté comme un détecteur fiable de factualité.

Pour un générateur réel, conserver les sources et vérifier séparément fidélité, citations et utilité. Un identifiant de citation valide prouve qu’un passage a été retrouvé; il ne prouve pas que toutes les affirmations ajoutées par un modèle sont soutenues. La réponse par défaut ne synthétise pas : elle reproduit les passages sélectionnés.

## 6. Expérience du jour
Observer l’ordre des candidats avant/après l’heuristique, mesurer les rangs documentaires et vérifier le contenu du contexte. Construire un exemple où le candidat manquant ne peut pas remonter. Montrer aussi qu’un budget trop faible force une abstention, sans transformer le manque de place en une prétendue absence de connaissance du corpus.

## À retenir
Le reranking affine la pertinence des candidats disponibles. Le packing et la fidélité des références font partie du contrat de réponse, sans devenir une preuve automatique de justesse.
