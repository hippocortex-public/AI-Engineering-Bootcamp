# Challenge — Agent de support stateful

## Objectif

Construire un agent de support client capable de maintenir un état conversationnel sur plusieurs tours.

L’agent doit gérer au moins trois intentions :

- suivi de commande ;
- remboursement ;
- problème technique.

## Contraintes fonctionnelles

### Intention `order_status`

Champs requis :

- `order_id` ;
- `email`.

### Intention `refund`

Champs requis :

- `order_id` ;
- `email` ;
- `reason`.

### Intention `technical_issue`

Champs requis :

- `email` ;
- `issue_summary`.

## Comportement attendu

L’agent doit :

1. initialiser un état par session ;
2. détecter ou conserver l’intention active ;
3. extraire les champs disponibles dans les messages ;
4. calculer les champs manquants ;
5. poser une seule question ciblée à la fois ;
6. passer à `ready_for_action` lorsque tous les champs requis sont présents ;
7. refuser d’exécuter une action si l’état est incomplet ;
8. sérialiser et restaurer l’état ;
9. empêcher la fuite d’état entre sessions.

## Exemple attendu

```text
Utilisateur : Je veux un remboursement.
Assistant : Quel est votre numéro de commande ?
Utilisateur : ORD-1001
Assistant : Quelle adresse email est associée à la demande ?
Utilisateur : lea@example.com
Assistant : Quelle est la raison de votre demande de remboursement ?
Utilisateur : J’ai été facturée deux fois.
Assistant : Merci, j’ai les informations nécessaires pour traiter la demande de remboursement.
```

## Livrables attendus

- une classe ou dataclass `ConversationState` ;
- une fonction `handle_user_message` ;
- une fonction `missing_required_fields` ;
- une fonction de sérialisation ;
- une fonction de restauration ;
- au moins six tests ;
- un court commentaire expliquant la différence entre state et memory.

## Critères de validation

Le challenge est réussi si :

- le comportement multi-tours fonctionne ;
- les sessions sont isolées ;
- les champs manquants sont corrects ;
- l’action n’est jamais déclenchée trop tôt ;
- l’état restauré est équivalent à l’état sauvegardé ;
- le code reste compréhensible et exécutable sans service externe.
