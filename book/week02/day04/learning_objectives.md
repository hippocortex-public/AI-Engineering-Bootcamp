# Objectifs pédagogiques — Conversation State

## Objectifs principaux

À la fin de cette journée, l’apprenant doit être capable de concevoir et coder un état conversationnel minimal pour un agent IA.

## Compétences visées

### 1. Compréhension conceptuelle

L’apprenant sait expliquer :

- ce qu’est un agent stateless ;
- pourquoi le stateless est insuffisant pour une conversation multi-tours ;
- la différence entre conversation history, conversation state et memory ;
- le rôle des slots métier ;
- le rôle du statut conversationnel ;
- le risque de fuite d’état entre sessions.

### 2. Conception backend

L’apprenant sait concevoir un objet d’état contenant :

- un identifiant de session ;
- un identifiant utilisateur ;
- un historique court ;
- une intention courante ;
- des champs collectés ;
- des champs manquants ;
- des résultats d’outils ;
- un compteur de tours ;
- un statut de progression.

### 3. Implémentation Python

L’apprenant sait implémenter :

- une dataclass représentant l’état ;
- une fonction d’initialisation ;
- une fonction de mise à jour à partir d’un message ;
- une fonction de détection de champs manquants ;
- une fonction de décision de prochaine réponse ;
- une sérialisation JSON ;
- une restauration depuis JSON.

### 4. Qualité et testabilité

L’apprenant sait écrire des tests vérifiant :

- que deux sessions restent isolées ;
- que les champs sont collectés progressivement ;
- qu’une intention détectée est conservée ;
- qu’un champ manquant déclenche une question ciblée ;
- qu’un état sérialisé puis restauré conserve les informations ;
- qu’un appel métier n’est pas déclenché avec des données incomplètes.

## Résultat attendu

L’apprenant doit produire un mini-agent de support client capable de conserver le contexte d’une demande sur plusieurs tours.

Le résultat attendu n’est pas un chatbot complet.

Le résultat attendu est une architecture claire, testable et extensible.

## Critères de réussite

La journée est validée si l’apprenant peut :

- définir précisément ce qui appartient à l’état conversationnel ;
- expliquer ce qui ne doit pas y être stocké ;
- tracer l’évolution de l’état sur plusieurs tours ;
- empêcher l’exécution prématurée d’une action ;
- sérialiser l’état sans perdre les informations critiques ;
- préparer le terrain pour la journée suivante sur la mémoire.
