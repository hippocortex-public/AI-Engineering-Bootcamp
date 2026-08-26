# Corrigé — Questions d’entretien — Jour 6

## Question 1

Le Prompt Engineering concerne la formulation des instructions. Le Context Engineering concerne la construction du contexte complet transmis au modèle : sources, état, mémoire, outils, ressources, budget, permissions et ordre.

## Question 2

Envoyer tout l’historique augmente le coût, la latence, le bruit et les risques de fuite. Cela peut aussi introduire des instructions obsolètes ou contradictoires.

## Question 3

Je sélectionne les outils selon l’objectif courant, les permissions, la criticité de l’action, le domaine de l’agent et le risque opérationnel. Un agent ne doit voir que les outils utiles à la tâche.

## Question 4

La memory est une connaissance persistante. Le state décrit la progression applicative courante. Le context est le sous-ensemble réellement injecté dans l’appel modèle.

## Question 5

Je définis un budget, j’estime le coût de chaque élément, je trie par priorité, je préserve les éléments critiques, puis je supprime, résume ou récupère partiellement les éléments moins importants.

## Question 6

Un context pack est un paquet structuré contenant les éléments sélectionnés, les éléments rejetés, les raisons de rejet, le coût estimé et le rendu final pour modèle.

## Question 7

MCP standardise l’exposition d’outils, ressources et prompts. Le Context Engineering décide lesquels de ces éléments doivent réellement être utilisés ou injectés.

## Question 8

J’utilise des niveaux de visibilité, des politiques par agent, des filtres explicites, des audits et des tests empêchant l’injection non autorisée.

## Question 9

Les signaux utiles incluent fraîcheur, source, score de pertinence, priorité métier, taille, type, confiance, agent cible et lien avec l’objectif.

## Question 10

Je conserve les IDs des éléments sélectionnés, les éléments rejetés, les raisons de rejet, le budget, l’agent cible, la politique utilisée et le rendu final haché ou versionné.
