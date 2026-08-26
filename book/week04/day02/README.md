# Semaine 4 — Jour 2 : Abstraction Agent

## Résumé

Après avoir posé l’architecture générale du mini-framework au jour 1, cette journée construit la première abstraction réellement réutilisable : `Agent`.

Un agent n’est pas seulement une fonction qui appelle un modèle. Dans un framework professionnel, un agent est un composant applicatif avec :

- une identité ;
- des instructions ;
- un contrat d’entrée ;
- un contrat de sortie ;
- une stratégie de construction de prompt ;
- une dépendance injectée vers un client modèle ;
- des garde-fous ;
- des métadonnées de trace ;
- une surface d’extension vers les tools, la mémoire et les workflows.

Cette journée reste volontairement avant le `Tool Registry`, qui arrive au jour 3. Le but est de construire une abstraction propre, testable et stable avant de lui connecter des capacités externes.

## Place dans la progression

```text
S4 J1 Architecture
   ↓
S4 J2 Abstraction Agent
   ↓
S4 J3 Tool Registry
   ↓
S4 J4 Memory Layer
   ↓
S4 J5 Workflow Engine
   ↓
S4 J6 Observabilité
   ↓
S4 J7 Intégration
```

## Livrables du jour

- comprendre le rôle d’une abstraction `Agent` dans un framework ;
- distinguer un agent, un runner, un model client et un tool ;
- concevoir une API simple et testable ;
- implémenter un agent déterministe pour les tests ;
- valider les invariants de configuration ;
- préparer les extensions futures sans coupler l’agent à ces extensions.

## Lab

Le lab implémente une abstraction d’agent en Python standard library :

```bash
python agent_abstraction.py
python test_agent_abstraction.py
```

Le code ne dépend d’aucune clé API afin de rester exécutable en local et en CI.
