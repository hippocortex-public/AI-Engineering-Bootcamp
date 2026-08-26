# Challenge — Construire un serveur MCP de support client

## Contexte

Vous travaillez sur un assistant IA de support client.

L’équipe veut exposer plusieurs capacités au futur client MCP :

- recherche de commande ;
- recherche dans la base de connaissance ;
- génération d’un brouillon de réponse ;
- remboursement contrôlé.

Vous devez concevoir et implémenter une première version du serveur MCP.

## Objectif

Étendre le lab pour produire un serveur MCP capable de gérer un scénario complet :

> Un agent reçoit un message client, recherche la commande, consulte la politique de remboursement, génère un brouillon de réponse et refuse toute action de remboursement sans approbation humaine.

## Contraintes

Le serveur doit :

1. exposer au moins 4 tools ;
2. exposer au moins 2 resources ;
3. exposer au moins 1 prompt ;
4. valider tous les arguments ;
5. refuser les propriétés supplémentaires ;
6. distinguer erreurs protocolaire et erreurs métier ;
7. produire une trace pour chaque requête ;
8. refuser `refund_order` sans `approved_by_human=true`.

## Scénario minimal

1. Appeler `tools/list`.
2. Appeler `lookup_order` avec `ORD-1001`.
3. Lire `kb://support/refunds`.
4. Appeler `create_support_draft`.
5. Tenter `refund_order` sans approbation.
6. Vérifier que le serveur refuse.
7. Tenter `refund_order` avec approbation.
8. Vérifier que le serveur retourne un résultat structuré.

## Critères d’acceptation

Le challenge est réussi si :

- tous les tests passent ;
- les erreurs sont structurées ;
- les sorties sont déterministes ;
- le code ne dépend d’aucun service externe ;
- la séparation tool/resource/prompt est claire ;
- les noms de tools sont compréhensibles par un modèle.

## Bonus

Ajoutez un champ `risk_level` aux tools :

- `read`
- `write`
- `sensitive`

Puis adaptez `tools/list` pour exposer ce niveau de risque.
