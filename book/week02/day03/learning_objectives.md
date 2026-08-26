# Objectifs pédagogiques — Structured Outputs

## Objectif principal

Savoir concevoir et valider des sorties structurées produites par un agent IA afin de les intégrer de manière fiable dans un backend applicatif.

## Compétences visées

À la fin de cette journée, l’apprenant doit être capable de :

1. Expliquer pourquoi une sortie texte libre est insuffisante pour un système agentique.
2. Décrire la différence entre :
   - texte libre ;
   - JSON libre ;
   - JSON mode ;
   - function calling ;
   - Structured Outputs.
3. Concevoir un schéma de sortie avec :
   - champs obligatoires ;
   - types explicites ;
   - valeurs énumérées ;
   - contraintes numériques ;
   - objets imbriqués ;
   - interdiction des propriétés non prévues.
4. Identifier les points de rupture d’une sortie générée :
   - JSON invalide ;
   - champ manquant ;
   - type incorrect ;
   - valeur hors enum ;
   - propriété supplémentaire ;
   - confiance non bornée.
5. Implémenter une validation côté application.
6. Transformer une sortie validée en objet métier Python.
7. Écrire des tests autour d’un contrat de sortie.
8. Relier les Structured Outputs à l’architecture d’un agent.

## Résultat opérationnel

L’apprenant doit être capable de construire le pipeline suivant :

```text
User request
→ Prompt
→ Model output
→ JSON parsing
→ Schema validation
→ Domain object
→ Business decision
```

## Critères de réussite

Une solution est considérée comme correcte si :

- elle ne dépend pas du texte libre pour prendre une décision ;
- elle valide le JSON avant usage ;
- elle échoue explicitement quand la sortie ne respecte pas le contrat ;
- elle sépare le schéma, le parsing, la validation et la logique métier ;
- elle contient des tests reproductibles ;
- elle peut être expliquée lors d’un entretien technique.

## Ce qui n’est pas l’objectif du jour

Cette journée ne vise pas encore à :

- gérer un historique conversationnel complet ;
- implémenter une mémoire long terme ;
- orchestrer plusieurs agents ;
- appeler un vrai fournisseur LLM en production ;
- optimiser les coûts ou la latence.

Ces sujets seront construits progressivement dans les jours et semaines suivants.
