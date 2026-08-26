# Exercices — Jour 6 — Context Engineering

## Exercice 1 — Identifier les couches de contexte

Classe les éléments suivants dans la bonne catégorie :

1. `Tu es un agent support interne.`
2. `ticket_id = T-204`
3. `L’utilisateur préfère les réponses courtes.`
4. `Dernier message : "Je n’ai toujours pas reçu la facture."`
5. `Ressource MCP : billing_policy.md`
6. `Outil : get_invoice_status`
7. `Trace : l’agent a déjà tenté get_customer_profile.`

Catégories possibles :

- instruction système ;
- état de tâche ;
- mémoire longue ;
- historique récent ;
- ressource ;
- outil ;
- trace.

## Exercice 2 — Construire un context pack

Pour la demande suivante :

```text
Pourquoi la facture F-392 est-elle bloquée ?
```

Contexte disponible :

```text
A. Instruction système support
B. Ancien ticket RH
C. État courant : invoice_id=F-392, customer=ACME
D. Mémoire : l’utilisateur préfère les réponses détaillées
E. Ressource : politique de relance facturation
F. Outil : get_invoice_status
G. Outil : delete_invoice
H. Trace ancienne d’un incident non lié
```

Sélectionne les éléments à injecter et justifie les exclusions.

## Exercice 3 — Budget

Tu disposes d’un budget de 100 tokens estimés.

Éléments disponibles :

| Élément | Tokens | Priorité |
|---|---:|---:|
| system | 20 | 100 |
| task_state | 30 | 95 |
| billing_policy | 70 | 80 |
| user_preference | 15 | 40 |
| old_trace | 25 | 10 |

Quels éléments sélectionnes-tu ?

## Exercice 4 — Visibilité

Explique pourquoi un élément `private` ne doit pas être injecté dans le contexte d’un autre agent sans transformation explicite.

## Exercice 5 — Déduplication

Deux éléments contiennent :

```text
Le client ACME a une facture F-392 bloquée.
```

et

```text
 le client acme a une facture f-392 bloquée. 
```

Explique pourquoi ils doivent être considérés comme doublons dans une déduplication normalisée.

## Exercice 6 — PII

Transforme ce contexte avant injection :

```text
Contacte Alice à alice@example.com ou au +33 6 12 34 56 78.
```

## Exercice 7 — MCP

Explique pourquoi un client MCP ne doit pas injecter automatiquement toutes les ressources exposées par un serveur MCP.

## Exercice 8 — Test d’architecture

Propose trois tests unitaires indispensables pour un moteur de Context Engineering.
