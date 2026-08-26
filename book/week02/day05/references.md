# Références — Memory courte, longue et state

## Documentation officielle

- OpenAI Agents SDK — Memory  
  https://openai.github.io/openai-agents-python/ref/memory/

- OpenAI Agents SDK — Session memory  
  https://openai.github.io/openai-agents-python/ref/memory/session/

- OpenAI Agents SDK — Running agents, sessions and context continuity  
  https://openai.github.io/openai-agents-python/running_agents/

- OpenAI API Reference — Conversations  
  https://platform.openai.com/docs/api-reference/conversations

- OpenAI Platform — Data controls and endpoint usage policies  
  https://platform.openai.com/docs/models/default-usage-policies-by-endpoint

## Concepts à retenir

- Une session conserve l’historique de conversation pour un contexte de travail.
- Une mémoire longue doit être distincte de l’historique brut.
- Une stratégie mémoire doit définir quoi écrire, quoi lire et quoi supprimer.
- Les données persistantes doivent être isolées par utilisateur.
- Une mémoire agentique doit être testée comme un composant applicatif.

## Lectures complémentaires

- Conception de systèmes stateful.
- Data minimization.
- Event sourcing appliqué aux conversations.
- Résumés incrémentaux sous contrainte de fenêtre de contexte.
- Tests d’isolation multi-tenant.

## Notes pour le bootcamp

Cette journée prépare directement :

- J6 Agent Loop & planification ;
- J7 Agent autonome ;
- Semaine 4 Memory Layer ;
- Semaine 8 Gouvernance ;
- Semaine 9 Mémoire d’agents dans les systèmes RAG.
