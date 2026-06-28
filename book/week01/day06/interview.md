# Interview — Jour 6

## Questions fondamentales

### 1. Quelle différence faites-vous entre une API de complétion et une API moderne orientée réponses ?

Une API de complétion prend souvent un prompt et retourne du texte. Une API moderne structure davantage l'interaction : instructions, messages, outils, formats de sortie, métadonnées et parfois événements. Elle est plus adaptée aux applications.

### 2. Pourquoi les Structured Outputs sont-ils importants en backend ?

Parce qu'un backend consomme des contrats. Une réponse libre oblige à parser du texte fragile. Une sortie structurée permet validation, stockage, routage et tests.

### 3. Est-ce qu'un schéma JSON garantit que le modèle a raison ?

Non. Il garantit seulement mieux la forme attendue. Le contenu peut rester faux, incomplet ou dangereux. Il faut conserver des validations métier.

### 4. Qu'est-ce qu'un Tool Call ?

C'est une demande structurée du modèle pour que l'application exécute une fonction déclarée. Le modèle choisit ou propose l'outil et ses arguments, mais l'application décide de l'exécution.

### 5. Pourquoi ne faut-il pas laisser le modèle exécuter directement un outil ?

Parce que l'application doit contrôler les permissions, les effets de bord, les coûts, les erreurs, les logs et les règles métier.

## Questions AI Engineering

### 6. Comment testez-vous un flux de Tool Calling sans appeler un fournisseur LLM ?

On simule la sortie du modèle avec une chaîne JSON déterministe, puis on teste le parseur, la validation, le registre d'outils et le comportement en cas d'erreur.

### 7. Où placez-vous les retries ?

Les retries peuvent être placés autour de l'appel modèle, autour du parsing structuré et autour des appels outils idempotents. Ils ne doivent pas masquer des erreurs de validation ou déclencher plusieurs fois une action non idempotente.

### 8. Quelle différence entre validation de schéma et validation métier ?

La validation de schéma vérifie la forme : types, champs requis, valeurs autorisées. La validation métier vérifie si le résultat est acceptable dans le contexte réel : droits, cohérence, règles internes, état du système.

### 9. Que loggez-vous dans un appel moderne ?

Au minimum : identifiant de corrélation, modèle, version du prompt ou des instructions, format demandé, outil demandé, arguments validés, latence, statut, erreurs et coût si disponible.

### 10. Quel est le risque d'exposer trop d'outils au modèle ?

Le modèle peut choisir un outil inadapté, produire des arguments incorrects, augmenter la latence ou créer une surface de risque plus grande. Il faut exposer le minimum utile pour la tâche.
