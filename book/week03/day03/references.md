# Références — MCP Server

## Références principales

- Model Context Protocol — Specification, section server/tools.
- Model Context Protocol — Server concepts: tools, resources, prompts.
- OpenAI Agents SDK — MCP integration.
- OpenAI Agents SDK — multi-agent orchestration and handoffs.

## À retenir

Le serveur MCP expose des capacités sous contrat.

Pour un AI Engineer, les points clés ne sont pas seulement l’API, mais :

- le design de surface d’outillage ;
- la validation ;
- la sécurité ;
- l’observabilité ;
- l’évolution des contrats ;
- la compatibilité avec des clients et agents différents.

## Lectures recommandées

1. Lire la section `tools/list`.
2. Lire la section `tools/call`.
3. Lire les recommandations de sécurité liées aux tools sensibles.
4. Observer comment un SDK d’agents connecte un agent à un serveur MCP.
5. Comparer MCP avec un simple registre local de fonctions.

## Notes d’implémentation

Le lab de ce jour est volontairement minimal.

Il n’implémente pas :

- transport stdio réel ;
- transport HTTP réel ;
- streaming ;
- authentification ;
- autorisation avancée ;
- découverte réseau.

Ces éléments relèvent d’une version production.
