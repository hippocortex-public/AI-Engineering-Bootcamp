# Corrigé — Questions d’entretien

## Question 1

Un `ToolRegistry` centralise la découverte, la description, la validation, l’autorisation, l’exécution et la traçabilité des tools disponibles pour un agent. Il sert de frontière entre le raisonnement du modèle et les capacités applicatives réelles.

## Question 2

La validation runtime reste obligatoire parce qu’une sortie structurée générée par un modèle n’est pas une garantie de sécurité. Le serveur doit protéger ses invariants même si le modèle se trompe, hallucine un champ, oublie un champ requis ou produit une valeur hors enum.

## Question 3

`failed` signifie que l’appel a échoué : outil inconnu, arguments invalides ou exception pendant l’exécution. `blocked` signifie que le système a volontairement refusé l’appel pour une raison de politique : outil désactivé, scope manquant ou approbation humaine absente.

## Question 4

Un outil comme `refund_customer` doit être marqué sensible, limité par scope, journalisé, soumis à approbation humaine, testé avec des montants limites et entouré de garde-fous métier. Le modèle ne doit jamais déclencher directement le remboursement final sans contrôle applicatif.

## Question 5

Exposer tous les outils augmente la surface d’attaque et le risque d’action non pertinente. Un agent doit recevoir seulement les capacités nécessaires à son rôle et à la tâche courante.

## Question 6

Une trace utile contient au minimum le nom du tool, l’instant de lookup, le résultat de validation, les décisions de politique, le statut final, le temps d’exécution, les erreurs normalisées et un identifiant de session ou de run.
