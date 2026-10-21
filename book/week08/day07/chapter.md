# S8 J7 — Projet de supervision et décision de livraison


## 1. Réunir les preuves sans les écraser
Le projet intègre cinq contrôles distincts. Quality reprend la décision et les cas critiques de J1. Performance contrôle p95 et erreurs techniques. Cost vérifie le coût par succès utile. Governance vérifie le manifeste. Security exécute la suite du contrôleur de permissions. La décision est la conjonction des cinq résultats.

Une somme pondérée peut masquer une violation de sécurité derrière un avantage financier. Le moteur garde donc un veto critique. Il affiche les contrôles qui échouent au lieu d’un score unique opaque. Une preuve absente, mal formée ou incompatible provoque une erreur de validation; elle n’est pas assimilée à un zéro rassurant ou à un contrôle non applicable.

## 2. Ce qui est réellement intégré
Les rapports d’évaluation sont recalculés depuis le dataset et les sorties de J1. Les observations synthétiques proviennent de examples/week08/fixtures. Le code vérifie la grille de trente-six essais et la cohérence du dataset, du workload et de la configuration. La grille de prix et la politique ont leurs propres preuves. La date de décision est explicite pour rendre le replay reproductible.

Les empreintes garantissent une comparaison locale de contenu. Le pipeline ne vérifie pas de signature ni d’attestation d’un environnement de collecte. Les acteurs et approbations sont fictifs. Le programme ne prétend pas être un service de gouvernance authentifié.

## 3. Deux versions, une conclusion instructive
La baseline obtient 10/12 aux cas de J1, p95=601 ms, aucun échec technique et un coût par succès utile de 0,002028 USD synthétique. Selon la politique du lab et la date du 20 octobre 2026, ses cinq contrôles passent.

Le candidat obtient 11/12, p95=461 ms et un coût utile plus faible. Son timeout conserve un maximum à 2200 ms et un taux d’erreur de 1/36, encore sous le seuil illustratif. Il reste refusé : c09 est une régression critique. Les tests du contrôleur peuvent passer en parallèle; ils ne remplacent pas le refus attendu dans les sorties de l’agent.

## 4. Codes de sortie exploitables
Le CLI produit 0 pour une décision acceptée, 1 pour une décision refusée et 2 pour une preuve invalide. Ce contrat évite de confondre refus métier et panne du moteur. Le rapport peut être écrit avec --output. Un rapport généré pour un refus est utile et doit être conservé comme preuve.

Le paquet livre une commande de validation locale. Il ne modifie aucun workflow CI existant et n’ajoute aucune action GitHub externe. Dans un pipeline, exécuter le moteur après les tests, conserver le rapport comme artefact et utiliser le code retour pour bloquer la suite. Aucun déploiement automatique n’est inclus.

## 5. Faire vivre la supervision
Le registre de version relie responsables, configuration, résultats et retour prévu. Le runbook décrit quoi examiner quand un contrôle se dégrade. Une alerte ne doit pas être supprimée en baissant simplement le seuil après observation du candidat. Toute modification de politique est une nouvelle décision, avec justification et nouvelle évaluation.

Avant un déploiement réel, ajouter un jeu réservé représentatif, une collecte contrôlée, des mesures en charge, une identité vérifiée et des essais de rollback. Un canary demande une allocation de trafic et des métriques comparables; copier le mot « canary » dans une procédure ne le met pas en œuvre. Le cours fournit le plan de revue, pas un opérateur d’infrastructure.

## 6. Présenter le projet comme ingénieur et architecte
Expliquer d’abord le problème : une meilleure moyenne a caché une régression critique. Montrer les preuves puis la décision restrictive. Décrire la frontière entre évaluation, métriques techniques, coût et permission. Terminer par une limite concrète et la prochaine expérience qui la réduirait.

Cette démarche complète vos compétences backend : contrat d’entrée strict, validation des données, codes de retour, invariants testés et traçabilité de version. Le composant IA ajoute une incertitude à mesurer; il n’efface pas les principes de conception d’un système exploitable.

## À retenir
La supervision utile relie une mesure à une décision et à une action. Une preuve critique défavorable ne disparaît ni dans la vitesse ni dans les économies.
