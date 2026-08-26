# Exercices — Jour 7 — Projet multi-agent

## Exercice 1 — Identifier les responsabilités

À partir du scénario suivant :

> Un utilisateur demande un plan de migration d’un assistant interne vers une architecture multi-agent avec MCP, état partagé et revue sécurité.

Identifiez les responsabilités qui doivent être séparées entre agents.

Répondez sous forme de tableau :

| Responsabilité | Agent | Sortie attendue |
|---|---|---|

## Exercice 2 — Définir un état partagé

Proposez cinq entrées d’état utiles pour le projet.

Pour chaque entrée, précisez :

- la clé ;
- le propriétaire ;
- la visibilité ;
- la raison de stockage.

## Exercice 3 — Construire un context pack

Pour un agent `security`, listez les informations qui doivent être incluses dans son contexte.

Listez aussi les informations qui ne doivent pas être incluses.

## Exercice 4 — Identifier les outils MCP

Proposez quatre outils que le système pourrait exposer via MCP.

Pour chaque outil, indiquez :

- nom ;
- description ;
- arguments requis ;
- sortie attendue ;
- sensibilité.

## Exercice 5 — Critères d’arrêt

Définissez les conditions qui doivent arrêter la boucle multi-agent.

Incluez au moins :

- une condition de succès ;
- une condition d’échec ;
- une condition de clarification utilisateur ;
- une condition de sécurité.

## Exercice 6 — Trace d’exécution

Écrivez un exemple de trace en JSON pour une exécution courte contenant :

- un événement de planification ;
- un appel d’outil ;
- une contribution d’agent ;
- une revue finale.

## Exercice 7 — Analyse de robustesse

Expliquez pourquoi il est risqué de laisser tous les agents accéder à tout l’état partagé.

Donnez deux exemples de bugs ou d’effets indésirables.
