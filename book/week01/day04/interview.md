# Interview — Questions Jour 4

## Questions fondamentales

### 1. Un token est-il équivalent à un mot ?

Non. Un token peut être un mot, un sous-mot, un caractère, un morceau avec espace, ou une partie d’un symbole. Le découpage dépend du tokenizer.

### 2. Pourquoi les LLM utilisent-ils des tokens ?

Parce qu’un réseau neuronal manipule des identifiants numériques et des vecteurs. Les tokens créent un pont entre texte brut et embeddings.

### 3. Qu’est-ce que BPE ?

Byte Pair Encoding est une méthode qui apprend à fusionner les paires d’unités les plus fréquentes pour construire un vocabulaire de sous-mots.

### 4. Pourquoi BPE est-il utile pour les mots inconnus ?

Un mot inconnu peut être représenté par plusieurs sous-mots connus. Le modèle n’a pas besoin d’un token complet pour chaque mot possible.

### 5. Pourquoi deux modèles peuvent-ils compter un nombre différent de tokens pour le même texte ?

Parce qu’ils peuvent utiliser des tokenizers, vocabulaires et règles de prétraitement différents.

## Questions AI Engineering

### 6. Comment la fenêtre de contexte influence-t-elle une architecture RAG ?

Elle limite le nombre de chunks injectables. Un RAG robuste doit donc sélectionner, classer, compresser et budgéter les documents avant l’appel modèle.

### 7. Que se passe-t-il si le prompt est trop long ?

L’appel peut échouer, être tronqué, coûter trop cher ou produire une réponse de mauvaise qualité à cause du bruit contextuel.

### 8. Pourquoi réserver un budget de sortie ?

Parce que la réponse générée consomme aussi des tokens. Si tout le budget est utilisé par l’entrée, le modèle ne peut pas produire une réponse suffisante.

### 9. Quelle métrique ajouteriez-vous dans une API LLM interne ?

Au minimum : tokens d’entrée, tokens de sortie, coût estimé, latence, modèle utilisé et raison d’échec éventuelle.

### 10. Faut-il entraîner son propre tokenizer pour utiliser une API LLM moderne ?

Non dans la majorité des cas. Il faut utiliser le tokenizer associé au modèle. Entraîner un tokenizer est pertinent pour construire ou adapter un modèle, pas pour appeler un modèle API existant.

## Réponse attendue senior

Un bon AI Engineer ne voit pas la tokenisation comme un détail bas niveau. Il la relie au coût, à la latence, à la qualité de récupération documentaire, à la mémoire conversationnelle, à la sécurité des prompts et à la robustesse de l’API.
