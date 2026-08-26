# Corrigé — Questions d'entretien

## Réponse 1

La mémoire conversationnelle sert à maintenir la continuité immédiate d'un dialogue. La mémoire durable conserve des informations réutilisables dans le futur, comme des préférences ou des faits vérifiés.

## Réponse 2

Le namespace empêche les fuites entre utilisateurs, tenants, équipes ou sessions. Sans namespace, une mémoire peut être réutilisée dans le mauvais contexte.

## Réponse 3

Toutes les mémoires ne sont pas pertinentes, autorisées ou à jour. L'injection automatique augmente le bruit, le coût, le risque de fuite et le risque d'instructions contradictoires.

## Réponse 4

Il faut identifier le namespace de l'utilisateur, supprimer toutes les mémoires associées, auditer l'opération et confirmer l'exécution. Les logs réglementaires éventuels doivent suivre la politique de conformité du produit.

## Réponse 5

Une préférence exprime une manière souhaitée d'interagir. Un fait vérifié décrit une information validée. Les deux ne doivent pas avoir la même durée de vie ni la même politique de partage.

## Réponse 6

La visibilité indique qui peut lire ou injecter la mémoire. Elle évite qu'une information privée soit partagée avec un agent ou un contexte non autorisé.

## Réponse 7

Le runner doit dépendre d'une interface `MemoryStore`, pas d'une classe concrète. PostgreSQL ou Redis deviennent alors des implémentations de cette interface.

## Réponse 8

Risques principaux : fuite inter-utilisateurs, stockage de PII, rétention excessive, réutilisation de données périmées, prompt injection persistante, confusion entre observation et fait.

## Réponse 9

Chaque écriture doit produire un événement : action, record, namespace, agent, version, timestamp. Une trace doit expliquer pourquoi une mémoire a été promue.

## Réponse 10

Une base vectorielle devient utile lorsque les mémoires sont nombreuses et que la recherche lexicalement exacte ne suffit plus. Elle doit rester derrière le contrat de la Memory Layer.
