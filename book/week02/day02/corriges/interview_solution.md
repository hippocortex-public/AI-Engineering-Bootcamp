# Corrigé — Questions d’entretien Function Calling

## 1. Qu’est-ce que le function calling ?

C’est un mécanisme par lequel un modèle produit une demande d’appel de fonction structurée, généralement avec un nom d’outil et des arguments. L’application reçoit cette demande, la valide, exécute éventuellement l’outil et renvoie le résultat.

## 2. Pourquoi le modèle ne doit-il pas exécuter directement les fonctions ?

Parce que le modèle n’est pas une frontière de sécurité. Il peut se tromper, halluciner un outil, produire des arguments invalides ou être influencé par une instruction malveillante. L’exécution doit rester contrôlée par l’application.

## 3. Outil déclaré vs fonction Python

L’outil déclaré est le contrat visible par le modèle. La fonction Python est l’implémentation réelle, côté application. Le modèle voit le contrat, pas nécessairement le code.

## 4. Pourquoi valider les arguments ?

Le schéma guide le modèle mais ne garantit pas que tous les outputs seront sûrs ou utilisables. La validation protège l’application contre les erreurs, les champs inattendus et les types incorrects.

## 5. Risque d’un outil générique

Un outil générique augmente l’ambiguïté et la surface d’action. Il devient difficile de contrôler ce qui est autorisé, de journaliser correctement et de tester le comportement.

## 6. Rôle du Tool Registry

Le registre centralise les outils disponibles, leurs schémas et leurs handlers. Il sert de couche de contrôle entre la sortie du modèle et l’exécution métier.

## 7. Appel vers un outil inconnu

L’application doit refuser l’appel et retourner une erreur structurée comme `UNKNOWN_TOOL`. Elle ne doit jamais chercher dynamiquement une fonction par nom dans le scope global.

## 8. Erreur d’outil

Une erreur propre contient au minimum :

```json
{
  "ok": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Message compréhensible"
  }
}
```

## 9. Lecture vs écriture

Un outil de lecture consulte un état. Un outil d’écriture modifie un état. Les outils d’écriture nécessitent plus de contrôle : permission, confirmation, idempotence et audit.

## 10. Confirmation utilisateur

Elle est nécessaire pour les actions irréversibles, coûteuses, sensibles ou susceptibles d’avoir un impact externe : annulation, paiement, suppression, email, changement de droits.

## 11. Logs utiles

Il faut journaliser le nom de l’outil, les arguments validés, le résultat, le statut, le code d’erreur, la durée et l’identifiant de conversation.

## 12. Tester sans vrai LLM

On remplace le modèle par un planificateur déterministe ou par des fixtures de tool calls. Les tests vérifient le registre, la validation et le dispatch.

## 13. Function calling vs Structured Outputs

Le function calling sert à demander une action applicative. Les Structured Outputs servent à contraindre une réponse structurée. Les deux utilisent des schémas, mais leur intention n’est pas la même.

## 14. Instruction malveillante

L’application ne doit pas exécuter une action uniquement parce qu’elle apparaît dans le texte utilisateur ou dans une proposition du modèle. Elle applique le registre, les permissions, la validation et les confirmations.

## 15. Où placer les permissions ?

Dans l’application. Le prompt peut rappeler les règles, mais il ne remplace pas une vérification déterministe côté serveur.

## Mise en situation

Le modèle peut proposer un appel à un outil d’annulation, mais l’application doit vérifier :

- que l’outil existe ;
- que l’utilisateur a le droit d’annuler ;
- que la commande est annulable ;
- qu’une confirmation explicite a été donnée.

Sans confirmation, l’application doit refuser l’exécution et journaliser une tentative d’action sensible.
