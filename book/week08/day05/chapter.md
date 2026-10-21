# S8 J5 — Gouvernance des versions et décisions


## 1. Gouverner une modification concrète
Un système IA change lorsque le modèle, le prompt, les outils, les données ou les droits changent. Conserver seulement le commit du backend laisse une partie du comportement sans version. La gouvernance doit permettre de répondre à une question simple : qui a autorisé quelle configuration, sur quelles preuves et avec quelle stratégie de retour ?

Le manifeste du cours décrit release_id, propriétaire, relecteur, empreinte de configuration, date limite, revue de risque et référence de rollback. Les identités sont fictives et les approbations sont des données de test. Le programme n’authentifie aucune personne et ne déploie rien.

## 2. Relier les objets sans confondre intégrité et confiance
Le dataset de J1 possède une empreinte canonique. Le lot de performance reprend cette empreinte et ajoute celles du workload et de la configuration. Le rapport final inclut une empreinte de toutes les preuves reçues. Un changement devient détectable quand on compare à une valeur de référence connue.

Une empreinte ne prouve ni l’auteur ni la véracité des mesures. Un acteur capable de remplacer fichier et hash peut fabriquer une cohérence locale. En exploitation, associer collecte contrôlée, artefacts protégés, provenance du pipeline et signatures selon le besoin. La liste des relecteurs du lab vient d’une politique locale; elle n’est pas un annuaire de confiance.

## 3. L’approbation porte sur un contenu précis
Le contrôleur compare config_hash du manifeste à la configuration observée dans les runs. Une différence produit configuration_changed et bloque la gouvernance. Il vérifie aussi approved, le relecteur autorisé, la séparation propriétaire/relecteur et la validité à la date explicite de décision.

La date valid_until est inclusive : une approbation au 20 novembre reste valable pour une décision datée du 20 novembre. Le replay utilise le 20 octobre 2026 par défaut pour reproduire le cours. Pour une décision opérationnelle, fournir la date réelle et une source d’horloge fiable. Changer une date d’entrée pour contourner une expiration ne serait pas un contrôle fiable.

## 4. Séparer les responsabilités
Le propriétaire prépare et documente la version. Le relecteur vérifie les preuves et autorise le périmètre prévu. L’exploitation surveille les signaux et peut déclencher le rollback selon le runbook. La séparation de fonctions du lab est une règle pédagogique; le niveau d’exigence réel dépend de l’organisation et du risque.

Éviter deux extrêmes : tout laisser au développeur sans preuve, ou multiplier les documents sans pouvoir relier une décision à la configuration livrée. Une exception doit avoir un responsable, un périmètre, une date et un traitement du risque résiduel. Le moteur du cours n’autorise aucune exception automatique aux cas critiques.

## 5. Préparer le retour avant le déploiement
rollback_ref identifie une version antérieure fictive. Sa présence rend le manifeste complet mais ne prouve pas la possibilité d’un retour effectif. Vérifier compatibilité des contrats, état durable, prompts, index et outils. Revenir au code précédent ne restaure pas une donnée supprimée ou un message déjà publié.

Le cours livre un modèle de registre et un runbook, sans opérateur de déploiement. Le projet final doit montrer un refus cohérent quand les preuves sont insuffisantes. Une décision locale accepted n’est pas une autorisation réelle d’exécuter une action dans un compte externe.

## 6. Rétention et confidentialité
Définir les informations à garder pour expliquer une décision et celles à exclure. Conserver rapports, références et hashes peut suffire pour des analyses agrégées; les exemples exacts demandent parfois un stockage séparé à accès limité. Une empreinte de texte sensible ne rend pas forcément ce texte anonyme, notamment si son domaine de valeurs est petit.

Le registre synthétique ne contient pas de données personnelles réelles. Les durées de rétention et responsabilités du modèle documentaire sont des choix pédagogiques à adapter, sans présenter ce cours comme une preuve de conformité juridique.

## À retenir
Une décision traçable relie des artefacts versionnés, des rôles et un périmètre. Le hash explique ce qui a changé; une chaîne de confiance explique pourquoi on peut croire les preuves.
