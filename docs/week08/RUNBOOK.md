# Runbook pédagogique — AI Engineering Ops

| Symptôme | Vérifier d’abord | Action prévue | Preuve de sortie |
|---|---|---|---|
| quality=false | Cas critiques, couverture, version de grille | Bloquer la décision et analyser la régression | Nouveau rapport sous protocole validé |
| p95 ou erreurs au-delà du seuil | Population, tentatives, dépendances, configuration | Limiter les nouveaux essais et diagnostiquer | Mesures comparables après correction |
| Coût utile trop élevé | Tokens, cache, reprises, succès utiles | Réduire les appels selon une politique évaluée | Budget et qualité vérifiés ensemble |
| Approbation expirée ou hash différent | Configuration réellement visée et relecteur | Nouvelle revue, sans modifier la date pour contourner | Manifeste lié et valide |
| Cas de permissions en échec | Tenant, rôle, outil et portée du grant | Bloquer l’action concernée | Tests positifs et négatifs corrigés |
| Preuve invalide, code 2 | JSON, doublons, grille et hashes | Corriger la collecte avant de décider | Rapport complet généré |

Le propriétaire prépare la preuve; le relecteur autorise le périmètre prévu; l’exploitation applique les procédures de sa propre organisation. Les noms du lab sont fictifs.

Le projet ne déploie ni ne revient en arrière. Avant de brancher un pipeline réel : identifier les artefacts de retour, vérifier leur compatibilité et tester la procédure dans un environnement isolé. Une publication externe déjà envoyée ne s’annule pas simplement en restaurant un conteneur.

Ne pas réutiliser les contenus de production comme fixtures publiques sans revue, minimisation et contrôle d’accès. Les seuils du cours ne sont pas des exigences de production.
