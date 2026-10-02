# Notes de revue — Jour 6

## Points à observer

- Le principal est immuable et vient du registre serveur.
- Les règles ne dépendent jamais du texte du modèle.
- L'accès documentaire est centralisé et couvert par plusieurs routes.
- La rotation de clé n'accorde pas un nouveau quota.
- Les erreurs et logs n'exposent pas les valeurs sensibles.
- Le démarrage sans identités valides échoue.

## Erreurs fréquentes

Faire confiance à `tenant` dans un JSON ; considérer une clé fournisseur comme une
identité client ; appliquer l'ACL après avoir envoyé le document au LLM ; traiter
un résultat d'outil comme du code ; partager une clé de cache entre tenants ; croire
qu'un test d'injection simulé certifie un modèle réel.

## Barème proposé

| Dimension | Points |
|---|---|
| Identité et permissions correctement expliquées | 4 |
| Isolation par tenant sur toutes les voies | 5 |
| Outils contrôlés et arguments validés | 4 |
| Quotas et logs correctement interprétés | 4 |
| Limites et migration production argumentées | 3 |

Réussite proposée : 14/20, sans fuite inter-tenant ni contournement d'outil dans le
lab. La validation pédagogique reste à effectuer par l'apprenant.

## Propositions d'amélioration

Sans modifier les spécifications : intégrer un IdP, un quota Redis atomique et un
jeu d'évaluation adversariale lorsque les composants de production seront réunis.
Ces propositions ne sont pas de nouveaux jours ni des modifications de roadmap.
