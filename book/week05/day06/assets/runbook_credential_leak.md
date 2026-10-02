# Runbook — Suspicion de fuite d'une clé API

## Déclencheurs

Clé retrouvée dans un dépôt ou journal, activité inhabituelle, tentative d'accès à
une ressource non autorisée. Une hausse de 401 ne prouve pas à elle seule une fuite.

## Actions

1. Identifier la clé compromise sans la recopier dans les tickets ou logs.
2. Retirer cette clé du registre de confiance. Dans ce lab, recharger la configuration
   exige de redémarrer l'application ; vérifier tous les processus concernés.
3. Émettre une nouvelle clé pour le même tenant/sujet et les seuls scopes nécessaires.
4. Vérifier que l'ancienne clé renvoie 401 et que la nouvelle conserve le quota du
   principal pendant le chevauchement avant retrait (le redémarrage remet le quota
   local à zéro : cette limite motive son stockage Redis en production).
5. Examiner l'audit par sujet, tenant, route et période. Préserver les preuves en
   limitant leurs lecteurs. Ne pas activer les logs de prompts pour ce diagnostic.
6. Rechercher la source : historique Git, CI, variables de build, proxy, APM, frontend.
7. Corriger cette source, vérifier l'isolation documentaire et surveiller les refus.

Une nouvelle clé n'efface pas une fuite passée. Les suites d'incident suivent le
processus de l'organisation et l'étendue réellement constatée.
