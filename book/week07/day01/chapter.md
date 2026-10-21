# Semaine 7 — Jour 1 : n8n et frontières du workflow


## 1. Le problème à résoudre
Une demande de support arrive depuis un formulaire. L’équipe souhaite l’enregistrer, préparer une réponse et demander une validation avant sa publication. Le workflow représente ce processus métier; les connecteurs exécutent les échanges entre systèmes. Ajouter un agent autonome pour piloter tout le parcours rendrait les règles de validation difficiles à contrôler. Nous réservons ici la génération du brouillon à un composant spécialisé et laissons le processus explicite.

n8n fournit une représentation visuelle des étapes et de leurs connexions. Un déclencheur reçoit une entrée; les nœuds manipulent des items et appellent des services. Un item porte généralement un objet `json`; un nœud peut produire plusieurs items. Ne supposez pas qu’une exécution contient toujours une seule demande. Pour ce lab, le contrat exige volontairement un objet événement par requête.

## 2. Les trois responsabilités
Le déclencheur détecte l’entrée du travail, la transformation prépare les données et l’effet modifie un système. Lire une facture n’a pas le même risque que publier une réponse. Dans notre exemple, recevoir l’événement écrit un job durable mais ne publie rien. Le service Python contrôle les transitions métier. n8n transporte les événements et déclenche périodiquement le traitement.

Ce choix permet de tester les invariants sans démarrer l’éditeur. Il est adapté à votre expérience backend : n8n joue le rôle d’un adaptateur d’intégration et le moteur celui d’un service applicatif. Il ne faut pas déplacer les règles de validation dans une succession d’expressions impossibles à tester. À l’inverse, coder tous les connecteurs en Python supprimerait une partie de l’intérêt de l’outil.

## 3. Premier parcours n8n
Importer le workflow `01_ingress.json`. Le nœud Webhook reçoit un POST et utilise une authentification par en-tête. Le nœud HTTP Request transmet `body` au backend. Respond to Webhook propage le résultat HTTP du backend. L’acceptation d’un événement nouveau produit 202; un doublon identique produit 200. Cette réponse confirme l’enregistrement, pas la fin du traitement.

L’URL de test est utilisée lorsque le nœud écoute une exécution manuelle. L’URL de production dépend d’un workflow publié ou activé selon l’interface de la version installée. Copier exactement l’URL affichée. Une erreur fréquente est d’envoyer à l’URL de test alors que personne n’écoute, ou d’oublier de rendre le workflow actif pour l’URL de production.

## 4. Environnement reproductible
La configuration Compose utilise des volumes séparés pour n8n et le backend. Le backend s’adresse à sa base SQLite; n8n conserve ses propres exécutions dans son volume. Ces bases ne sont pas interchangeables. Le nom DNS `backend` fonctionne entre conteneurs du projet Compose; `localhost` dans le conteneur n8n désigne n8n lui-même. Depuis votre terminal, utiliser `127.0.0.1:8080`.

Les tokens restent dans des credentials et dans le fichier `.env` local. L’export JSON ne contient aucune valeur secrète. Le lab utilise HTTP sur la boucle locale, avec cookies non sécurisés pour cette seule installation locale. Un environnement partagé demanderait TLS et une gestion d’identité différente.

## 5. Pourquoi commencer par un double déterministe ?
Le générateur fourni est une fonction à règles, explicitement marquée comme simulation. Il sépare le comportement du processus de la variabilité d’un modèle. Si un doublon publie deux fois une réponse, ce défaut existe indépendamment du fournisseur LLM. Aujourd’hui, observez l’acceptation; les jours suivants introduiront les transitions et les erreurs.

## À retenir
Une exécution n8n est un passage technique dans le graphe. Un job métier peut survivre à plusieurs exécutions. Les credentials, le contrat HTTP et l’état durable constituent la frontière entre ces deux niveaux.
