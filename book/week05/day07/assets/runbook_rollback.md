# Runbook — Retour à l'image précédente

## Conditions

Référence précédente conservée, secret/configuration cohérents, schéma compatible,
volumes préservés. Identifier la cause possible par statuts, logs et métriques.
Ne pas afficher les prompts ou clés pour diagnostiquer.

## Procédure locale

1. Vérifier la compatibilité de la base ; si elle est rompue, utiliser un plan
   de récupération ou correction explicite, pas un rollback aveugle.
2. Restaurer la référence précédente avec `up --no-deps --no-build --wait` sur api.
3. Vérifier readiness puis les scénarios `smoke_test.py`.
4. Observer les erreurs et la latence après retour.
5. Conserver les volumes ; ne pas utiliser `down --volumes`.
6. Documenter commit/image/configuration avant et après, et la cause du refus.

Un rollback refusé ou une ancienne release encore indisponible nécessite une
intervention. Un quota atteint par des tentatives répétées ne se traite pas en
supprimant arbitrairement le registre de consommation.
