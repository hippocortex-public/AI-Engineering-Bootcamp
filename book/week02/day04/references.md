# Références — Conversation State

## Références principales

- OpenAI Agents SDK — Sessions.
- OpenAI Agents SDK — Running agents.
- OpenAI Agents SDK — Agents.
- OpenAI Platform — Responses API.
- OpenAI Platform — Function calling.
- OpenAI Platform — Structured Outputs.

## Concepts à revoir

- Conversation history.
- Session.
- Slot filling.
- State machine.
- Serialization.
- Idempotency.
- Session isolation.
- Personally identifiable information.
- Short-term state vs long-term memory.

## À retenir

Un framework ou une API peut aider à gérer l’historique de conversation.

Mais l’état métier d’un agent reste une responsabilité applicative.

Pour un AI Backend Engineer, le point clé est de concevoir un state :

- explicite ;
- minimal ;
- validable ;
- isolé par session ;
- sérialisable ;
- observable ;
- sécurisé.
