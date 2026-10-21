# S10 J3 — Résumé extractif, couverture et fidélité


## 1. Quel résumé produire ?
Un résumé peut aider à consulter un ticket, préparer une transmission ou réduire un contexte. Ces usages ne demandent pas les mêmes informations. Identifier les faits nécessaires : composant, symptôme, impact, action et incertitude. Un résumé court mais privé de la condition d’une action peut être dangereux même s’il reste fluide.

Le lab choisit un résumé extractif. Il reproduit des phrases du texte sans en générer de nouvelles. Cette méthode rend les références simples à vérifier, mais elle ne garantit pas que les phrases retenues sont les plus importantes ni que leur combinaison garde toutes les nuances.

## 2. Segmenter sans perdre les positions
sentence_spans sépare après une ponctuation suivie d’espace ou sur des lignes. Les décimales comme 1,5 et les adresses contenant un point sans espace restent dans leur segment. Les offsets pointent dans le texte original; chaque phrase retenue doit correspondre à source[start:end].

Ce segmentateur n’est pas un analyseur linguistique général. Des abréviations, dialogues ou listes peuvent le tromper. Les tests couvrent quelques formats du corpus, pas toutes les conventions du français. Modifier les règles demande une réévaluation des références et budgets.

## 3. Centralité TF-IDF
Chaque phrase est vectorisée. Le centroïde des vecteurs de phrases donne une représentation moyenne du document. La similarité avec ce centroïde classe les phrases par centralité lexicale. Ce calcul local non supervisé ne réutilise pas le vocabulaire du classifieur de J1 et n’utilise pas les résumés de référence pour choisir les phrases.

Une phrase répétant les termes fréquents peut être centrale sans contenir l’impact critique. Une phrase unique portant une négation importante peut être mal classée. La centralité est une heuristique à inspecter, pas une mesure de vérité ni d’importance universelle.

## 4. Budget et ordre
Le sélecteur conserve des phrases entières qui tiennent dans word_budget et s’arrête à max_sentences. Les phrases retenues sont ensuite remises dans l’ordre source pour faciliter la lecture. Un grand segment peut être sauté au profit d’un suivant plus court. Si rien ne tient, le statut budget_exhausted le signale.

Le budget est un nombre de mots séparés par espaces, pas un budget de tokens LLM. Ne pas comparer directement ce nombre aux tokens d’une API. Pour alimenter un modèle réel, compter aussi instructions, question, wrappers et réserve de sortie avec son tokenizer.

## 5. Mesurer ce que l’on sait mesurer
Le rapport fournit un chevauchement multiensemble de tokens avec une référence écrite. Ce proxy donne précision, rappel et F1 lexicaux. Ce n’est pas ROUGE, ce n’est pas une mesure de factualité et ce n’est pas une appréciation humaine d’utilité.

Le contrôle d’offsets prouve que chaque phrase existe dans la source. Il ne prouve pas que le résumé couvre toutes les affirmations importantes ni qu’il présente correctement leur relation. Une campagne plus utile annoterait les unités d’information et les omissions critiques, puis comparerait les méthodes sous le même protocole.

## 6. Du résumé extractif au génératif
Un modèle génératif peut reformuler et fusionner, mais ajoute un risque d’affirmations non soutenues. Garder le texte source, les références et une politique de revue. Le lab n’en exécute aucun; il prépare les contrôles que ce raccord devra conserver. Un extracteur de phrases n’est pas une preuve de « zéro hallucination » au sens d’une compréhension correcte.

## À retenir
La compression doit préserver le contrat d’information. La fidélité des slices, le recouvrement lexical et l’utilité du résumé sont trois questions différentes.
