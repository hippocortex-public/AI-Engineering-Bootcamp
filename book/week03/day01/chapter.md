# Chapitre — Architectures multi-agents

## 1. Pourquoi passer au multi-agent ?

Un agent autonome mono-agent peut comprendre une demande, planifier, appeler des outils, observer les résultats, maintenir un état et produire une réponse.

Mais un seul agent devient difficile à contrôler lorsque la tâche demande plusieurs expertises, plusieurs validations ou une séparation stricte entre décision et exécution.

Un système multi-agents est utile lorsque le problème nécessite :

- plusieurs domaines métier ;
- une validation indépendante ;
- une exécution parallèle ;
- un routage explicable ;
- une réduction de la complexité d’un prompt unique ;
- une meilleure traçabilité des responsabilités.

Le multi-agent n’est pas automatiquement meilleur. Il ajoute de la latence, du coût, des risques de boucle et plus de surface de debug.

La bonne question est :

> La séparation en plusieurs agents réduit-elle réellement le risque ou la complexité du système ?

## 2. Définition pratique d’un agent

Dans ce bootcamp, un agent est une unité d’exécution composée de :

- un rôle ;
- des instructions ;
- un périmètre ;
- des entrées attendues ;
- des sorties attendues ;
- des outils autorisés ;
- des contraintes ;
- éventuellement une mémoire ou un état.

Un agent n’est pas seulement un prompt. C’est un composant d’architecture.

## 3. Pattern manager-worker

Dans un pattern manager-worker, un manager garde le contrôle de la conversation et délègue des sous-tâches à des spécialistes.

```text
Utilisateur → Manager → Spécialiste A
                     → Spécialiste B
                     → Reviewer
           ← Réponse consolidée
```

Ce pattern est utile lorsque :

- une réponse finale unique doit être produite ;
- le manager doit agréger plusieurs résultats ;
- les spécialistes ne doivent pas parler directement à l’utilisateur ;
- les garde-fous doivent être centralisés.

Risques :

- manager trop puissant ;
- perte d’information lors de la synthèse ;
- coût élevé si trop de spécialistes sont appelés.

## 4. Pattern handoff

Dans un handoff, un agent transfère le contrôle à un autre agent. Le spécialiste devient responsable de la suite du tour ou de la session.

```text
Utilisateur → Triage → Agent Facturation → Réponse
```

Ce pattern est utile lorsque :

- la demande appartient clairement à un domaine ;
- le spécialiste doit répondre directement ;
- ses instructions doivent remplacer celles du routeur.

Risques :

- mauvais routage initial ;
- perte de contexte ;
- transferts successifs ;
- frustration utilisateur.

## 5. Pattern router

Le router choisit le chemin. Il ne résout pas la demande.

Une bonne décision de routage est structurée :

```json
{
  "target_agent": "billing",
  "confidence": 0.82,
  "reason": "The user asks about an invoice.",
  "requires_clarification": false
}
```

Le router doit demander une clarification si la confiance est faible ou si plusieurs catégories sont possibles.

## 6. Pattern parallèle

Plusieurs agents peuvent travailler simultanément sur des sous-tâches indépendantes :

```text
Question
├── Agent Recherche
├── Agent Calcul
└── Agent Risques
        ↓
Synthèse
```

Ce pattern est utile pour réduire la latence ou comparer plusieurs points de vue. Il exige ensuite un agrégateur robuste.

## 7. Pattern reviewer

Un reviewer vérifie une réponse candidate.

Il peut :

- valider ;
- rejeter ;
- lister des problèmes ;
- demander une correction ;
- déclencher une revue humaine.

Il ne doit pas devenir un second producteur métier non contrôlé.

## 8. Contrats entre agents

Un contrat minimal contient :

```text
agent_name
responsibility
input_schema
output_schema
allowed_tools
handoff_conditions
failure_modes
trace_fields
```

Sans contrat, les agents deviennent des prompts informels difficiles à tester.

## 9. État partagé

Tout ne doit pas être partagé avec tous les agents.

| Élément | Partage recommandé |
|---|---|
| Message utilisateur courant | Oui |
| Décision de routage | Oui |
| Trace d’exécution | Oui côté système |
| Historique complet | Sous condition |
| Mémoire long terme | Sous condition stricte |
| Données sensibles | Besoin minimal |
| Raisonnement interne | Non |

L’état partagé doit être minimal, explicite et sérialisable.

## 10. Observabilité

Chaque étape doit produire une trace :

```json
{
  "step": 3,
  "agent": "reviewer",
  "action": "validate_answer",
  "status": "passed",
  "detail": "response respects constraints"
}
```

Les traces servent à comprendre le système, pas à exposer un raisonnement privé à l’utilisateur.

## 11. Quand éviter le multi-agent ?

Il faut éviter le multi-agent lorsque :

- la tâche est simple ;
- un seul domaine métier existe ;
- la latence est critique ;
- les rôles ne sont pas clairs ;
- il n’existe aucune stratégie de test ;
- les coûts sont supérieurs au bénéfice.

Un système multi-agents mal conçu peut être moins fiable qu’un agent unique.

## 12. Exemple : support SaaS

Architecture possible :

```text
User
 ↓
Triage Agent
 ├── Billing Agent
 ├── Refund Agent
 ├── Technical Agent
 └── Product Agent
        ↓
Reviewer Agent
        ↓
Final Answer
```

Pourquoi ce design ?

- Le triage évite un prompt unique trop large.
- Les spécialistes ont des responsabilités nettes.
- Le reviewer réduit le risque de réponse non conforme.
- Les traces rendent le système débogable.

## 13. À retenir

Un système multi-agents professionnel est une architecture logicielle avec responsabilités, contrats, routage, état partagé, limites, traces et tests.
