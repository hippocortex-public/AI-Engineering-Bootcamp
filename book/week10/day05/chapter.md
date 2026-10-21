# S10 J5 — Adaptation légère et contrôle des poids


## 1. Adapter sans tout réentraîner
Une adaptation légère modifie une partie ciblée du système plutôt que tous ses paramètres. Le coût, les données nécessaires et les risques dépendent des paramètres choisis. Avant un grand modèle, le lab montre un cas entièrement exécuté : un vocabulaire/IDF TF-IDF figé et une tête linéaire déjà entraînée que l’on continue à optimiser.

Cette expérience est une adaptation de tête de classifieur, pas un fine-tuning de LLM ni une exécution LoRA. La distinguer évite de confondre le principe de gel des représentations avec les mécanismes d’un Transformer. Le dossier optionnel propose une vraie boucle LoRA SEQ_CLS sur modèle BERT local, non exécutée ici.

## 2. Ce qui reste fixe
Le vectoriseur est appris sur les 36 exemples train. Les 12 exemples adapt passent seulement par transform. Un terme nouveau absent du vocabulaire ne crée pas une nouvelle caractéristique. La tête peut modifier les poids de caractéristiques connues; elle ne peut pas apprendre une colonne qui n’existe pas.

adapt_head clone le modèle initial avant partial_fit. Le modèle baseline reste donc disponible pour la comparaison. Le code vérifie que la partition fournie est adapt et que le nombre d’epochs est un entier positif. Dans une expérience réelle, conserver en plus les artefacts, versions et paramètres d’optimisation.

## 3. Sélection contrôlée
Le lab essaie 1, 3 et 8 epochs, choisis avant de voir les résultats. Il sélectionne le meilleur macro-F1 de validation et départage une égalité en faveur du plus petit nombre d’epochs. Le seuil de décision est également choisi sur validation. Aucun texte test n’entre dans le fit ni la sélection.

Les trois variantes peuvent être à égalité sur ce corpus facile. Un résultat sans amélioration est une conclusion valide : l’adaptation a changé les poids, mais elle n’a pas démontré de bénéfice sur le test. Il ne faut ni fabriquer un gain ni choisir la meilleure valeur de test parmi plusieurs essais.

## 4. Régressions et oubli
Une adaptation sur un sous-domaine peut améliorer ses cas et dégrader l’ancien domaine. Comparer la baseline et le candidat sur un protocole stable, puis observer les résultats par catégorie. Une moyenne peut cacher une régression minoritaire. Avec peu d’exemples, la mesure est instable et doit être complétée avant une décision réelle.

Un mélange de rappel d’anciennes données, une régularisation ou une représentation différente peut aider selon la tâche. Le cours ne les applique pas automatiquement. Tout changement du vocabulaire exige de réentraîner une tête compatible plutôt que d’utiliser des poids d’une autre dimension.

## 5. LoRA : un autre mécanisme
LoRA ajoute des matrices de faible rang sur certaines couches d’un modèle préentraîné, en conservant les poids de base gelés. Le choix des modules dépend de l’architecture. Le script optionnel cible explicitement BERT, query/value et une tête classifier sauvegardée, plutôt que supposer les mêmes noms pour tout modèle.

Le script utilise des artefacts locaux, une sélection sur validation et n’exécute pas le test. PyTorch, Transformers, PEFT et le modèle ne sont pas disponibles dans la validation obligatoire. La boucle est fournie comme expérience à vérifier dans un environnement verrouillé, sans annoncer de score LoRA.

## 6. Persister sans confondre hash et confiance
Le module exporte vocabulaire, IDF, poids, classes, seuil et provenance dans un JSON sans pickle. La relecture contrôle formes, valeurs finies et empreinte de contenu. Cela permet un aller-retour d’inférence testable. Le hash détecte une modification par rapport à une référence fiable; il ne signe pas l’auteur et ne protège pas contre un remplacement coordonné du fichier et du hash.

## À retenir
Une adaptation est réussie si son protocole est correct et son intérêt mesuré, y compris quand le résultat conclut à une absence de gain.
