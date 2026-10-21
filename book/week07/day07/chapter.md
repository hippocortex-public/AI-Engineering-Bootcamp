# Semaine 7 — Jour 7 : Projet intégré et revue d’architecture


## 1. Le livrable de la semaine
Vous disposez d’un moteur transactionnel local, d’une API HTTP et de trois workflows n8n. Le parcours complet reçoit une demande, génère un brouillon simulé, attend une décision et écrit une publication locale. Le projet démontre la maîtrise du processus autour d’une capacité IA remplaçable. Il ne publie ni email, ni ticket, ni message dans un service externe.

Le premier workflow transmet un événement. Le deuxième, planifié, appelle tick. Le troisième reçoit une décision explicite et appelle le endpoint de revue. Les workflows utilisent des credentials séparés et ne contiennent aucun secret. Le backend constitue la source d’état métier; les historiques d’exécution n8n servent au diagnostic du transport.

## 2. Contrat de démonstration
Préparer quatre cas : demande nominale approuvée, demande refusée, livraison répétée et demande expirée. Les scripts Python simulent l’horloge pour le cas d’expiration. Le parcours HTTP local démontre les rôles et la réponse 202. L’intégration n8n demande Docker et une configuration des credentials dans l’éditeur; elle possède sa propre checklist.

Le nominal ne suffit pas à prouver la fiabilité. Envoyer un même event_id avec un autre texte doit échouer. Faire échouer le générateur trois fois doit terminer le traitement automatique. Répéter une approbation doit laisser une seule publication. Un mauvais hash ou une identité non autorisée doit être rejeté avant l’effet.

## 3. Une revue doit distinguer preuve et intention
La suite unittest couvre le moteur et l’API en conditions locales. Les notebooks contiennent des exemples déterministes issus de sources Markdown. Les exports n8n sont des fichiers de configuration proposés pour import; sans exécution dans l’éditeur, leur validation reste statique. Le rapport livré indique exactement ce qui a été exécuté.

Ne transformez pas un scénario simulé en preuve de tenue en charge. Le serveur est séquentiel, le tick est borné à cent jobs et la base est SQLite. Un arrêt brutal, une saturation réseau, une corruption de stockage ou des workers concurrents demanderaient des tests supplémentaires. Le projet est un incrément pédagogique qui peut être intégré sans remplacer mini_framework ou ai_platform.

## 4. Note d’architecture
Présenter le problème, les responsabilités, les invariants et les alternatives. Pour ce lab, un backend isolé possède l’état; n8n possède les connecteurs et déclencheurs. Une alternative place plus de logique dans n8n, avec moins de code mais davantage de dépendance à la représentation des nœuds. Une autre utilise un moteur durable dédié, avec un protocole de reprise plus riche et un coût d’exploitation différent.

La décision doit partir des contraintes : nombre de workflows, équipe de maintenance, durée d’attente, besoin de transactions, débit et gouvernance des credentials. Éviter de choisir un outil parce qu’il comporte des capacités agentiques. L’agent est un composant du système, pas une réponse universelle à l’orchestration.

## 5. Passage vers une architecture exploitable
Pour un effet réel, prévoir une outbox et un dispatcher; pour plusieurs workers, un claim atomique et une politique de lease; pour plusieurs relecteurs, une identité individuelle et une autorisation par ressource. Pour le modèle, définir un jeu d’évaluation, les budgets et les garde-fous. Ces éléments sont des propositions d’amélioration documentées, pas des garanties déjà implémentées.

L’exploitation doit distinguer temps de génération, temps d’attente humaine et âge des jobs bloqués. Un SLO de réception peut être respecté alors que les demandes attendent des heures en revue. Les contrôles de la semaine 8 prolongeront cette analyse en traitant l’évaluation, les coûts et la gouvernance. Cette semaine reste centrée sur le workflow.

## À retenir
Un projet intégré est terminé lorsque son parcours et ses échecs attendus sont démontrables, ses fichiers reproductibles et ses limites clairement exposées.
