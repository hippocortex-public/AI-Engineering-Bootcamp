# Rejeu de paiement avec Kafka

Pour rejouer un paiement avec Kafka dans ce laboratoire, conserver les événements et les offsets du groupe consommateur. Le rejeu relit les événements du topic, puis applique un contrôle d’idempotence sur payment_id avant l’appel au fournisseur.

Réinitialiser les offsets ne garantit pas l’unicité de l’effet externe. Si le fournisseur accepte une clé d’idempotence, réutiliser une clé stable pour le paiement. Sinon, prévoir une réconciliation avant de rejouer une opération incertaine.

Les valeurs et procédures décrites sont des conventions du corpus fictif de formation. Elles ne décrivent aucun système bancaire réel.
