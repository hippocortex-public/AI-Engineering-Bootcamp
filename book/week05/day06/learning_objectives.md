# Objectifs pédagogiques — S5 J6

À la fin de la journée, vous devez pouvoir :

1. Distinguer authentification, autorisation et identité technique du fournisseur LLM.
2. Construire un principal issu d'une configuration serveur fiable.
3. Vérifier une permission de route et l'appartenance d'une ressource au tenant.
4. Appliquer une liste d'outils autorisés et valider leurs arguments.
5. Expliquer pourquoi une instruction dans un document ne confère aucun droit.
6. Limiter les appels d'une identité sans dépendre de son adresse IP.
7. Journaliser les décisions sans conserver les données sensibles.
8. Écrire des tests négatifs d'accès et identifier leurs limites.

## Preuves attendues

| Compétence | Preuve |
|---|---|
| Authentification | Clé inconnue refusée par les trois routes protégées |
| Isolation | Même document refusé par route directe, chat et outil |
| Autorisation des outils | `shell` et `http_fetch` refusés |
| Quotas | Rotation de clé ne réinitialisant pas le quota du sujet |
| Confidentialité | Absence de prompt et de clé dans les captures de logs |
| Jugement d'architecte | Plan d'intégration OIDC, Redis et PostgreSQL motivé |

## Ce qui relève d'une étape ultérieure

Le lab ne fournit pas de serveur OIDC, de JWT, de moteur de modération, de sandbox
système ni de quota distribué. Il ne mesure pas la résistance d'un vrai LLM aux
injections. Il montre les contrôles déterministes qui doivent entourer ce modèle.
