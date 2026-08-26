# Références — Coordination multi-agents

## Documentation principale

- OpenAI Agents SDK — Agent orchestration  
  https://openai.github.io/openai-agents-python/multi_agent/

- OpenAI Agents SDK — Handoffs  
  https://openai.github.io/openai-agents-python/handoffs/

- OpenAI Agents SDK — Agents  
  https://openai.github.io/openai-agents-python/agents/

- OpenAI — A practical guide to building agents  
  https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/

## Préparation MCP

- Model Context Protocol — Specification  
  https://modelcontextprotocol.io/specification/

- Model Context Protocol — Tools  
  https://modelcontextprotocol.io/specification/2025-06-18/server/tools

## Concepts à retenir

- Un handoff transfère le contrôle conversationnel.
- Un agent appelé comme outil exécute une sous-tâche sans nécessairement prendre le contrôle.
- Un manager central améliore souvent la traçabilité.
- Une coordination multi-agent doit être bornée, observable et testable.
- MCP est utile pour standardiser l'accès aux outils et contextes, mais il ne remplace pas la politique de coordination applicative.

## Lectures complémentaires

- Patterns : manager-worker, router-specialist, critic-reviewer, pipeline, debate.
- Concepts : traces, handoffs, context filtering, conflict resolution, deterministic orchestration.
