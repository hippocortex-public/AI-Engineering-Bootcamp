# Challenge — Concevoir une architecture production d’assistant support

## Contexte

Tu dois concevoir l’architecture d’un assistant support IA pour une plateforme SaaS.

L’assistant doit :

- recevoir une demande utilisateur via API ;
- récupérer le ticket concerné ;
- lire l’historique client ;
- produire une réponse structurée ;
- proposer une action ;
- déclencher un remboursement uniquement après validation humaine ;
- tracer chaque étape ;
- limiter le coût par requête ;
- ne jamais exposer de PII dans les logs.

## Travail demandé

Produis :

1. Un diagramme Mermaid.
2. Un blueprint JSON.
3. Une analyse des risques.
4. Une checklist de readiness.
5. Une stratégie de rollback.

## Contraintes

Ton architecture doit contenir au minimum une API, un service applicatif, un runtime agentique, un model gateway, un tool gateway, un state store, un memory store, une business database, une couche d’observabilité, une validation humaine, une limite d’itérations et une limite de coût.
