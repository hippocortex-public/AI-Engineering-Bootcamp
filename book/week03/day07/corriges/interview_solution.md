# Corrigé — Questions d’entretien — Jour 7 — Projet multi-agent

## Réponse 1

Un projet multi-agent ne doit pas être conçu comme une simple liste d’agents, car l’enjeu principal est l’orchestration. Il faut définir les responsabilités, les échanges, l’état partagé, les outils autorisés, les critères d’arrêt et les mécanismes de revue.

## Réponse 2

Un agent raisonne ou décide dans un périmètre donné. Un outil exécute une capacité bornée avec des entrées et sorties définies. Un agent peut choisir d’appeler un outil, mais l’outil ne possède pas de responsabilité autonome de workflow.

## Réponse 3

Le coordinateur reçoit l’objectif, construit le plan, sélectionne les agents, prépare le contexte, déclenche les actions, collecte les artefacts et décide du statut final selon la revue.

## Réponse 4

Chaque agent doit recevoir uniquement les informations utiles à sa tâche. Un contexte trop large augmente le bruit, les coûts, les risques de fuite et les erreurs de raisonnement.

## Réponse 5

MCP aide à standardiser l’intégration des outils. Un client peut découvrir les tools exposés par un serveur, comprendre leurs schémas d’entrée et les appeler de manière uniforme.

## Réponse 6

Un état partagé versionné permet de détecter les conflits, d’auditer les changements et de comprendre l’évolution d’un workflow. Sans version, deux agents peuvent écraser silencieusement leurs contributions.

## Réponse 7

`private` signifie visible seulement par le propriétaire. `shared` signifie visible par certains rôles autorisés. `public` signifie visible par tous les agents du workflow.

## Réponse 8

Une revue finale indépendante limite l’auto-validation. Elle permet d’évaluer la cohérence, la complétude, la sécurité et la qualité d’un résultat produit par d’autres agents.

## Réponse 9

Une boucle doit s’arrêter en cas de succès validé, d’objectif ambigu, de budget dépassé, d’action sensible non approuvée, d’absence d’agent compétent ou de revue négative.

## Réponse 10

Il faut tracer l’objectif, le plan, les agents appelés, les context packs, les outils utilisés, les modifications d’état, les artefacts produits, les erreurs, les décisions de revue et le statut final.
