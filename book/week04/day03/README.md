# Semaine 4 — Jour 3 : Tool Registry

## Résumé

Après avoir construit l’abstraction `Agent`, cette journée ajoute le composant qui permet à un agent d’agir : le `ToolRegistry`.

Un outil n’est pas simplement une fonction Python appelée par hasard. Dans un framework professionnel, un outil doit être décrit, validé, filtré, exécuté et tracé. Le registre d’outils sert de frontière entre le raisonnement du modèle et le monde applicatif.

Le but du jour est de construire un registre capable de :

- déclarer des tools avec un contrat stable ;
- exposer uniquement les outils autorisés ;
- valider les arguments avant exécution ;
- bloquer les actions sensibles sans approbation ;
- vérifier les scopes applicatifs ;
- retourner un résultat normalisé ;
- produire des traces exploitables par l’observabilité.

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

- comprendre le rôle d’un registre d’outils dans un framework agentique ;
- définir un contrat de tool indépendant du fournisseur LLM ;
- implémenter une validation d’arguments sur un sous-ensemble JSON Schema ;
- gérer les outils sensibles et les permissions ;
- transformer une fonction Python en tool déclaratif ;
- tester les cas d’erreur avant intégration dans l’agent.

## Lab

Le lab utilise uniquement la standard library Python.

Depuis la racine du projet :

```bash
python book/week04/day03/labs/tool_registry_lab.py
python book/week04/day03/labs/test_tool_registry.py
```

Le composant principal est placé dans :

```text
mini_framework/tool_registry.py
```
