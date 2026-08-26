# Corrigé — Exercices — Jour 7 — Projet multi-agent

## Exercice 1 — Identifier les responsabilités

| Responsabilité | Agent | Sortie attendue |
|---|---|---|
| Découper le travail | Planner | Plan ordonné et tâches spécialisées |
| Extraire le contexte | Researcher | Notes, contraintes et ressources utiles |
| Concevoir l’architecture | Engineer | Proposition technique structurée |
| Vérifier les risques | Security | Risques, blocages et recommandations |
| Contrôler la qualité | Reviewer | Score, verdict et commentaires |
| Orchestrer | Coordinator | Statut final, trace et agrégation |

Le point important est de ne pas confondre production et validation. L’agent qui produit une proposition ne doit pas être le seul à l’évaluer.

## Exercice 2 — Définir un état partagé

| Clé | Propriétaire | Visibilité | Raison |
|---|---|---|---|
| `objective` | coordinator | public | Objectif stable du workflow |
| `plan` | planner | shared | Tâches distribuables |
| `research.notes` | researcher | shared | Informations utiles aux autres agents |
| `security.risks` | security | shared | Risques à prendre en compte |
| `final.review` | reviewer | public | Décision finale auditable |

Une entrée privée possible serait `researcher.raw_notes`, qui peut contenir du bruit ou des éléments inutiles aux autres agents.

## Exercice 3 — Construire un context pack

Pour l’agent `security`, il faut inclure :

- l’objectif ;
- la proposition technique ;
- les outils utilisés ;
- les actions sensibles envisagées ;
- les contraintes de données ;
- les critères d’acceptation ;
- les décisions déjà prises.

Il ne faut pas inclure :

- les brouillons privés du researcher ;
- les détails non pertinents de planning ;
- l’historique complet de conversation ;
- les hypothèses abandonnées ;
- les informations personnelles inutiles.

## Exercice 4 — Identifier les outils MCP

| Outil | Description | Arguments requis | Sortie | Sensibilité |
|---|---|---|---|---|
| `search_knowledge_base` | Recherche dans une base documentaire | `query` | Notes textuelles | Faible |
| `generate_architecture` | Produit un squelette d’architecture | `objective`, `constraints` | Proposition | Moyenne |
| `create_test_plan` | Génère un plan de test | `artifact_name` | Liste de tests | Faible |
| `request_deployment_approval` | Demande une validation humaine | `action`, `reason` | Approbation/refus | Forte |

L’outil de déploiement ou d’approbation doit être protégé.

## Exercice 5 — Critères d’arrêt

Conditions possibles :

- succès : revue finale validée avec un score supérieur au seuil ;
- échec : budget d’étapes dépassé ;
- clarification : objectif trop vague ou absence d’agent compétent ;
- sécurité : action sensible demandée sans approbation ;
- révision : reviewer identifie des manques critiques.

## Exercice 6 — Trace d’exécution

```json
[
  {
    "step": 1,
    "actor": "planner",
    "event": "plan_created",
    "summary": "3 tasks generated"
  },
  {
    "step": 2,
    "actor": "researcher",
    "event": "tool_called",
    "tool": "search_knowledge_base"
  },
  {
    "step": 3,
    "actor": "engineer",
    "event": "artifact_created",
    "artifact": "architecture_proposal"
  },
  {
    "step": 4,
    "actor": "reviewer",
    "event": "review_completed",
    "score": 0.91,
    "verdict": "approved"
  }
]
```

## Exercice 7 — Analyse de robustesse

Donner tout l’état à tous les agents est risqué pour trois raisons.

Premièrement, cela augmente le bruit. Un agent peut utiliser une information non pertinente et produire une réponse moins fiable.

Deuxièmement, cela augmente le risque de fuite. Des notes privées ou des informations sensibles peuvent être réutilisées dans la réponse finale.

Troisièmement, cela complique le debug. Si tout le monde peut lire et écrire partout, il devient difficile de comprendre pourquoi une décision a été prise.
