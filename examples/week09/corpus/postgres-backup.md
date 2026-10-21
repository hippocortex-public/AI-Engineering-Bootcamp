# Sauvegarde et restauration PostgreSQL

Une sauvegarde PostgreSQL doit être vérifiée par une restauration dans un environnement isolé. Le succès d’une commande de sauvegarde ne démontre pas que la restauration respecte le délai et le point de reprise attendus.

Le runbook fictif demande de contrôler la cohérence des données restaurées et les droits applicatifs avant la remise en service. Les objectifs de reprise sont des décisions métier à définir séparément.
