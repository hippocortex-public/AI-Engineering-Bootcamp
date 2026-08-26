# Objectifs pédagogiques — MCP Client

## Objectifs principaux

À la fin de cette journée, l'apprenant saura :

1. expliquer le rôle d'un client MCP dans une architecture agentique ;
2. distinguer serveur MCP, client MCP, agent et orchestrateur ;
3. décrire le cycle `initialize → tools/list → tools/call` ;
4. convertir des tools MCP en outils utilisables par un agent ;
5. valider les arguments avant un appel serveur ;
6. interpréter les résultats et erreurs JSON-RPC ;
7. intégrer cache, traces et politiques de sécurité côté client.

## Compétences AI Engineering

L'apprenant sera capable de :

- concevoir une couche d'intégration protocolaire ;
- découpler l'agent des serveurs d'outils ;
- limiter les appels invalides grâce à la validation locale ;
- produire des traces auditables ;
- implémenter un registre d'outils dynamique ;
- préparer une architecture compatible multi-serveurs MCP.

## Ce que l'apprenant ne doit pas confondre

| Concept | Rôle |
|---|---|
| Agent | Raisonne, planifie, sélectionne une capacité |
| MCP Server | Expose des tools, resources ou prompts |
| MCP Client | Découvre, valide et appelle les capacités du serveur |
| Tool Registry | Vue locale des capacités disponibles |
| Transport | Canal d'échange JSON-RPC |
| Guardrail | Politique de contrôle avant ou après action |

## Résultat attendu

L'apprenant doit pouvoir implémenter un client qui expose une interface simple :

```python
client.initialize()
tools = client.list_tools()
result = client.call_tool("search_ticket", {"ticket_id": "INC-42"})
```

Puis adapter ces tools pour un agent :

```python
registry = client.as_agent_tools()
registry["search_ticket"]({"ticket_id": "INC-42"})
```
