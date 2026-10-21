# S8 J4 — Coûts, budgets et arbitrages


## 1. Donner un sens au coût unitaire
Un coût par requête ne dit pas combien coûte une résolution utile. Si une réponse échoue et nécessite deux reprises, les trois appels peuvent être facturés pour un seul résultat. Il faut préciser l’unité : tentative, demande, conversation ou tâche métier achevée. Le lab additionne trente-six tentatives et divise par le nombre d’essais techniquement réussis associés à un cas fonctionnel réussi.

Cette définition est locale : elle réutilise l’étiquette de qualité de J1 pour les trois essais de chaque cas. Elle ne prouve pas que trois générations indépendantes seraient correctes. La baseline totalise trente succès utiles selon ce proxy; le candidat trente-deux. Un timeout reste facturé dans la fixture, avec les tokens synthétiques fournis.

## 2. Calculer sans double comptage
Le compteur input_tokens inclut cached_input_tokens. Il faut soustraire le cache avant d’appliquer le tarif normal. La formule est : coût = ((entrée−cache) × prix_entrée + cache × prix_cache + sortie × prix_sortie) / 1000000. Les prix du cours sont inventés, nommés synthetic et exprimés en USD par million de tokens. Ils ne décrivent aucun tarif commercial.

Le module utilise Decimal avec des valeurs décimales sous forme de chaînes. Cela évite de construire un décimal à partir d’un flottant binaire déjà arrondi. Additionner avant d’arrondir les résultats d’affichage. Valider les compteurs et refuser le cache supérieur au total entrant. Un coût négatif ne doit jamais améliorer une décision.

## 3. Lire le rapport
La baseline coûte 0,06084 USD pour 36 tentatives, soit 0,002028 USD par succès utile selon le proxy. Le candidat coûte 0,05004 USD et 0,00156375 USD par succès utile. Cette amélioration n’autorise pas la livraison : c09 reste un échec critique.

Le coût complet d’un système inclut aussi outils, stockage, observabilité, réseau, calcul et intervention humaine. Le lab calcule seulement des tokens avec une grille synthétique. Si une tâche ne produit aucun succès, usd_per_success vaut null; ce n’est ni zéro ni un succès économique. La décision intégrée refuse ce cas.

## 4. Observer et limiter sont deux fonctions différentes
Un rapport de coût après l’appel ne bloque pas une dépense. Le composant Budget réserve un montant maximal avant l’admission, puis règle le coût observé. Un budget de 0,01 autorise une réservation de 0,008 mais refuse une deuxième réservation simultanée du même montant. Après règlement à 0,003, une partie du plafond redevient disponible.

La réservation suppose que la borne maximale soit crédible : limite de sortie, nombre d’appels et politique de retries doivent être maîtrisés. Le code refuse un règlement supérieur au plafond pour signaler une incohérence; il ne peut pas annuler une facture fournisseur déjà engagée. Le ledger est en mémoire et séquentiel, sans garantie entre processus ou après crash.

## 5. Arbitrer sans supprimer les obligations
Réduire le contexte, mettre en cache, changer de modèle ou borner les reprises peut réduire les coûts. Chaque modification demande une nouvelle évaluation et une mesure comparable. Éviter de tronquer le contexte métier nécessaire ou de retirer les refus de sécurité pour obtenir un meilleur score financier.

Des règles simples peuvent router les tâches faciles vers une option moins chère. Il faut cependant mesurer les erreurs de routage et le coût des escalades. Une politique de fallback multiplie parfois les appels. L’objectif n’est pas le prix du premier appel, mais le coût d’un résultat conforme au contrat.

## À retenir
Le coût utile garde les échecs dans le numérateur et définit le succès dans le dénominateur. Le budget d’admission complète la mesure comptable; il ne remplace pas la qualité ni la sécurité.
