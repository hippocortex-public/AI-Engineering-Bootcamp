# Évaluer avant de décider

## 1. Transformer un besoin en contrat

« Le chatbot répond bien » ne décrit aucun test. « Pour une demande de remboursement admissible, il indique le délai de 30 jours et ne modifie aucun dossier sans autorisation » expose deux obligations différentes. Décrire pour chaque cas une entrée, un contexte, une attente et une gravité. Fixer les critères avant d’observer les résultats pour éviter de déplacer le seuil au bénéfice d’une version.

L’unité peut être une réponse, un appel d’outil, une trajectoire d’agent ou l’état final d’un environnement. Une phrase correcte ne prouve pas qu’un outil a été exécuté correctement. Une trajectoire inhabituelle peut cependant parvenir à un état final valide. Évaluer les contraintes de sécurité séparément du succès fonctionnel.

Dans ce lab, les appels d’outils sont des objets à comparer. Ils ne sont jamais exécutés. Tester une autorisation réelle demanderait un environnement isolé et la vérification de ses effets.

## 2. Construire un jeu utile

Commencer par des scénarios représentatifs : tâches fréquentes, ambiguïtés, erreurs d’entrée et comportements interdits. Ajouter les incidents observés après anonymisation et revue. Ne pas mélanger données personnelles de production et fixtures distribuées.

Chaque ligne JSONL contient un identifiant stable, un type, une catégorie, une entrée, une attente et un indicateur critique. Les douze cas du lab couvrent réponses, objets structurés, appels d’outils et refus. Les entrées sont volontairement descriptives : ce sont des tests du moteur, pas des prompts prêts à être soumis à un fournisseur.

Séparer un jeu de développement, utilisé pour améliorer le système, d’un jeu réservé à la validation. Limiter l’accès au second et tracer les changements. Réutiliser continuellement le même jeu pour optimiser les prompts finit par favoriser ses particularités. Une empreinte permet de détecter un changement ; elle ne démontre ni représentativité ni absence de fuite.

## 3. Choisir le bon évaluateur

| Méthode | Utilisation | Limite |
|---|---|---|
| Comparaison exacte | Structure, nom et arguments d’outil | Rejette des variantes équivalentes hors contrat |
| Expressions attendues | Vérification locale de formulations | N’établit ni factualité ni absence de contradiction |
| Revue humaine | Nuance, utilité, cas à fort impact | Coût et désaccord entre annotateurs |
| Modèle évaluateur | Assistance sur des critères sémantiques | Biais, variabilité et sensibilité aux consignes |

Une réponse « ce n’est pas 12 euros » passe le critère lexical « 12 euros ». Ce défaut connu impose une revue ou un critère sémantique pour évaluer la justesse. Le lab conserve ce proxy pour rendre son comportement transparent.

Pour un évaluateur humain, fournir une grille, des exemples et une procédure de désaccord. Pour un modèle évaluateur, conserver sa version et son prompt, calibrer ses décisions sur un échantillon annoté et inspecter faux positifs et faux négatifs. Traiter le contenu évalué comme une donnée susceptible de contenir des instructions malveillantes.

## 4. Scores et couverture

Pour N cas, le taux global est le nombre de réussites divisé par N. Un cas absent reste dans le dénominateur et échoue. La couverture mesure le nombre de sorties présentes divisé par N : une couverture complète ne prouve aucune qualité.

Le taux micro donne le même poids à chaque cas. Le taux macro est la moyenne des taux par catégorie ; une petite catégorie pèse alors autant qu’une grande. Toujours afficher les effectifs pour éviter qu’un score sur deux observations paraisse solide.

Ici, la baseline obtient 10/12 et le candidat 11/12. Le candidat améliore c03 et c04, mais régresse sur c09, un refus inter-tenant critique. La règle accepte une version seulement si la couverture est complète, si le taux atteint 0,8 et si tous les cas critiques passent. La baseline est acceptée par cette règle locale ; le candidat est refusé.

Deux observations de sécurité ne permettent pas d’estimer un taux de risque en production. Ces seuils sont pédagogiques et doivent être justifiés par les conséquences, les exigences et la distribution des tâches avant tout usage réel.

## 5. Comparaison appariée et traçabilité

Comparer les mêmes identifiants avec le même dataset et la même grille. Répertorier améliorations et régressions au lieu de conserver seulement une différence de moyenne. Toute modification du protocole appelle une nouvelle baseline.

Le rapport inclut les empreintes du jeu, des sorties et de la grille. Il ne stocke pas le texte des sorties. Pour une collecte réelle, ajouter commit du système, version du prompt, fournisseur, modèle, paramètres, contexte d’outils, dates et répétitions. Les erreurs d’adaptateur doivent devenir des échecs traçables sans divulguer de secrets.

## 6. Variabilité et décision

Les fixtures donnent toujours le même résultat. Un modèle et ses outils peuvent varier. Répéter les cas, conserver chaque essai, analyser la dispersion et les erreurs par segment. Ne pas sélectionner uniquement le meilleur essai. Une évolution du fournisseur ou du corpus exige une nouvelle mesure.

Une évaluation avant livraison et l’observation en production se complètent. La première teste un contrat sur un jeu connu ; la seconde détecte des situations et distributions nouvelles. Un incident peut alimenter un nouveau cas après validation, sans remplacer le jeu réservé par les seuls incidents.

## 7. Procédure de revue

1. Vérifier l’intégrité des entrées et la couverture.
2. Inspecter les cas critiques et les erreurs par catégorie.
3. Comparer les versions sous le même protocole.
4. Appliquer les seuils et documenter les exceptions autorisées par le responsable.
5. Enregistrer une décision avec limites, preuves et date.

Le rapport du lab automatise une règle locale ; la responsabilité de livraison reste une décision située. Une bonne moyenne ne neutralise pas une violation critique.
