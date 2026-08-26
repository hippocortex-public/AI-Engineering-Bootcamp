# Review — Week 02 Day 01

## Synthèse pédagogique

Cette journée introduit l’architecture agentique comme un problème d’ingénierie logicielle.

Le point central est la séparation des responsabilités :

- état ;
- décision ;
- outil ;
- observation ;
- réponse ;
- trace.

## Ce que l’apprenant doit retenir

Un agent n’est pas simplement un prompt plus long.

Un agent est une orchestration structurée autour d’un modèle ou d’une logique de décision.

## Signaux de compréhension

L’apprenant est capable de :

- dessiner une architecture d’agent ;
- expliquer le rôle de chaque composant ;
- coder un agent minimal ;
- lire une trace d’exécution ;
- identifier les limites d’un agent déterministe.

## Erreurs fréquentes

### Erreur 1 — Tout mettre dans une seule fonction

Cela rend le système difficile à tester et à faire évoluer.

### Erreur 2 — Confondre état et mémoire

L’état concerne l’exécution courante.

La mémoire persiste au-delà de l’exécution courante.

### Erreur 3 — Appeler les outils sans garde-fou

Un agent qui peut déclencher des outils externes doit être contrôlé.

### Erreur 4 — Ne pas tracer les décisions

Sans trace, l’agent devient opaque.

## Préparation du jour 2

Le jour 2 remplacera progressivement une décision codée à la main par du function calling.

Le contrat d’architecture reste le même :

```text
input -> state -> decision -> tool -> observation -> answer
```

## Critères de validation de la journée

- Tous les fichiers Markdown obligatoires existent.
- Les corrections sont locales.
- Le lab est exécutable.
- Le notebook étudiant exclut les corrections.
- Le notebook enseignant inclut les corrections.
- Les diagrammes sont présents.
