# Corrigé de l'entretien

1. Image : code et runtime versionnés. Démarrage : configuration, secrets et accès
   aux données. Les données et clés client ne doivent pas être intégrées à l'image.
2. L'ordre initial ne protège pas contre une panne ultérieure. Timeouts, réponses
   contrôlées, reconnexion et politique de retry doivent vivre dans l'application.
3. Liveness constate le processus ; readiness sa capacité à servir le contrat. Ne
   pas redémarrer l'API en boucle pour une indisponibilité SQL externe.
4. L'UID est une identité Linux du processus. IAM contrôle le cloud ; le principal
   API représente un client. Ces autorités ne s'accordent pas automatiquement.
5. Oui si l'ACL n'est pas revalidée. Le lab relit le document avant tout cache hit et
   partitionne la clé par tenant et sujet. La révocation reste effective.
6. Utiliser un état partagé et une mutation atomique. Redis Lua évite l'intercalation
   entre contrôle et incrément. Définir la conduite lors d'une panne du limiteur.
7. Le tag peut être déplacé ; la base de l'image et les dépendances transitives
   peuvent varier. Conserver digest, lock, plateforme et provenance du build.
8. `down` retire les conteneurs/réseaux gérés tout en conservant les volumes nommés.
   `--volumes` retire ceux de la stack ; ce n'est pas une étape habituelle de rollback.
9. Compatibilité du schéma et des données avec l'ancienne image, disponibilité de
   cette image et revalidation. Expand/contract maintient une fenêtre de retour.
10. Un timeout ne prouve pas l'absence de consommation. Borner sorties et retries,
    réserver les budgets, rapprocher les appels et gérer l'idempotence des actions.

## Mise en situation

La readiness prouve la disponibilité des dépendances, pas l'attribution correcte
des scopes. Examiner les métadonnées des identités et la politique de route, puis
les changements de schéma de cache et de contexte d'autorisation. Comparer au
comportement précédent avec un compte de test autorisé.

Conserver la release seulement si les écarts sont attendus et acceptés. Si les
utilisateurs légitimes ont perdu l'accès, restaurer la version/configuration
compatible précédente et vérifier les scénarios métier. Ne pas diminuer les
permissions pour rendre tous les appels 200 ni exposer les clés dans les logs.
