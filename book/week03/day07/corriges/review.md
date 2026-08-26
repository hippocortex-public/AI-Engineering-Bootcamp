# Review formateur — Jour 7 — Projet multi-agent

## Ce que l’apprenant doit avoir compris

L’apprenant doit comprendre que le projet multi-agent est un système logiciel, pas une mise en scène de rôles.

Les points clés sont :

- un agent possède une responsabilité ;
- un outil possède une interface ;
- MCP standardise l’exposition de capacités ;
- l’état partagé doit être contrôlé ;
- le contexte doit être construit ;
- la boucle doit avoir des limites ;
- la sortie doit être revue ;
- la trace doit expliquer le résultat.

## Erreurs fréquentes

### Erreur 1 — Donner tout le contexte à tout le monde

Cela produit du bruit, augmente les risques de fuite et rend le debug difficile.

### Erreur 2 — Confondre agent et outil

Un outil ne décide pas. Il exécute.

### Erreur 3 — Multiplier les agents sans responsabilités stables

Ajouter des agents augmente la complexité. Il faut une raison d’architecture.

### Erreur 4 — Laisser l’agent producteur valider son propre résultat

Cela crée un risque d’auto-confirmation.

### Erreur 5 — Oublier les critères d’arrêt

Un agent autonome ou semi-autonome doit être borné.

## Grille d’évaluation

| Critère | Attendu |
|---|---|
| Architecture | Coordinator-led ou handoff contrôlé |
| État | Versionné, filtré, auditable |
| Contexte | Adapté par agent |
| Outils | Déclarés, validés, bornés |
| MCP | Interface standardisée ou simulée correctement |
| Sécurité | Actions sensibles protégées |
| Tests | Succès, échec, sécurité, trace |
| Sortie | JSON sérialisable et statut contrôlé |

## Questions de débrief

1. Quel agent pourrait être supprimé sans perte de responsabilité ?
2. Quelle information ne devrait jamais être rendue publique ?
3. Où placeriez-vous une validation humaine ?
4. Comment remplaceriez-vous les fonctions déterministes par des appels LLM ?
5. Quelles métriques ajouteriez-vous en production ?

## Propositions d’amélioration

Ces propositions ne modifient pas les spécifications du bootcamp. Elles sont des pistes optionnelles pour une future version du lab :

- ajouter un stockage SQLite pour rejouer les traces ;
- ajouter un export OpenTelemetry pédagogique ;
- ajouter un mode CLI ;
- ajouter une version utilisant un vrai serveur MCP local ;
- ajouter une évaluation automatique des artefacts finaux.
