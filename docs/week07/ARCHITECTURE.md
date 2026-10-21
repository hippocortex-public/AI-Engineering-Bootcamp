# Note d’architecture — Workflow de support hybride

## Contexte

Une demande de support doit être reçue de façon durable, enrichie par une proposition puis validée avant publication. Les événements et décisions peuvent être répétés et un traitement peut être interrompu. Le projet doit rester testable sans fournisseur IA.

## Décision pour le lab

n8n possède les déclencheurs et adaptateurs HTTP. Le backend possède le contrat, l’état métier et les transitions. Le générateur est injecté par un port; le double déterministe n’a aucune capacité de publication. Tous les brouillons exigent une décision humaine.

La publication est une ligne dans SQLite, committée avec la transition terminale. Les identifiants d’événements et de publications sont uniques. Le service est mono-processus et séquentiel : le paquet ne démontre pas la concurrence entre workers.

## Alternatives

| Option | Bénéfice | Coût ou limite |
|---|---|---|
| Logique principalement dans n8n | Graphe visible et moins de code | Invariants et tests liés aux nœuds |
| n8n et backend explicite, retenu | Connecteurs visuels et règles testables | Deux frontières à diagnostiquer |
| Moteur durable dédié | Primitives de reprise et attente plus riches | Infrastructure supplémentaire |

Cette décision correspond au laboratoire; elle n’est pas une recommandation universelle de production.

## Invariants

1. L’événement est committé avant l’accusé de réception.
2. Un identifiant accepté ne change pas de payload.
3. Le générateur prépare une proposition sans la publier.
4. Une décision porte sur le hash courant, un acteur autorisé et un délai valide.
5. Une décision identique répétée n’ajoute pas de publication locale.
6. Une erreur permanente ou un budget épuisé arrête les reprises.

## Fenêtres de panne

| Fenêtre | Comportement du lab | Architecture étendue |
|---|---|---|
| Commit d’ingestion réussi, réponse perdue | Livraison répétée reconnue | Rétention des clés |
| Génération finie, commit absent | Génération peut se répéter | Budget de coûts |
| Décision committée, réponse perdue | Décision identique reconnue | Même garde côté API |
| Envoi externe réussi, accusé perdu | Aucun envoi externe ici | Idempotence destinataire ou réconciliation |
| Deux workers cherchent un job | Hors périmètre | Claim, lease et fencing |

## Intégration au dépôt

Les ajouts sont confinés aux chemins week07 et scripts dédiés. Aucun fichier racine partagé et aucun export cumulatif mini_framework ou ai_platform n’est remplacé. Ce module n’affirme pas être déjà branché sur l’API de S5 : son port décrit le raccord à effectuer lorsque les interfaces courantes du dépôt sont disponibles.

## Propositions d’amélioration

Outbox avant effet externe; identité OIDC; claim avant plusieurs workers; instrumentation de l’âge des jobs; adaptateur LLM évalué. Ces propositions ne modifient aucune spécification gelée.
