# Références — Function Calling

## Références internes

- Semaine 2 Jour 1 — Architecture d’un agent.
- Semaine 2 Jour 3 — Structured Outputs.
- Mini-projet de Semaine 2 — Assistant IA mono-agent.

## Références conceptuelles

- Tool calling comme contrat entre modèle et application.
- JSON Schema pour représenter les arguments attendus.
- Validation applicative avant exécution.
- Séparation lecture / écriture dans les outils.
- Observabilité des appels d’outils.

## Références fournisseur

- Documentation OpenAI Platform — Responses API.
- Documentation OpenAI Platform — Function calling / tools.
- Documentation OpenAI Platform — Structured Outputs.

## À lire avec attention

Lorsqu’un fournisseur LLM propose du function calling, il faut distinguer :

1. la **déclaration des outils** envoyée au modèle ;
2. la **sortie structurée** produite par le modèle ;
3. l’**exécution réelle** faite par votre application ;
4. la **réponse finale** visible par l’utilisateur.

## Recommandation d’étude

Ne commencez pas par brancher un outil réel sur une API de production.

Commencez par :

1. simuler les appels ;
2. valider localement ;
3. écrire des tests ;
4. ajouter les logs ;
5. connecter ensuite un fournisseur LLM.
