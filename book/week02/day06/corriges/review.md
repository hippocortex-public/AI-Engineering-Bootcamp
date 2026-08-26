# Review formateur — Jour 6

## Résumé pédagogique

Cette journée introduit la compétence centrale du développement agentique : construire une boucle contrôlée autour du modèle.

L'apprenant doit comprendre qu'un agent fiable n'est pas un prompt autonome, mais une orchestration logicielle.

## Points à vérifier

Le formateur doit vérifier que l'apprenant sait expliquer :

- ce qu'est une boucle agentique ;
- pourquoi une limite d'itérations est obligatoire ;
- pourquoi l'état doit être explicite ;
- comment une observation modifie le state ;
- quand demander une clarification ;
- comment tester une boucle sans LLM réel.

## Questions de relance

- Que se passe-t-il si l'outil retourne une erreur ?
- Quelle différence entre un plan et une action ?
- Pourquoi faut-il journaliser les itérations ?
- Comment empêcher un agent de répéter la même action ?
- Quelle information doit rester dans le state et quelle information doit aller en mémoire longue durée ?

## Erreurs fréquentes à surveiller

1. L'apprenant confond planification et exécution.
2. L'apprenant met toute la logique dans le prompt.
3. L'apprenant oublie la condition d'arrêt.
4. L'apprenant ne valide pas les outils.
5. L'apprenant ne distingue pas action et observation.
6. L'apprenant invente des données manquantes.

## Évaluation rapide

L'apprenant est prêt pour le Jour 7 s'il peut concevoir une boucle qui :

- extrait ou demande les informations nécessaires ;
- appelle les bons outils ;
- observe les résultats ;
- met à jour l'état ;
- termine avec un statut clair ;
- produit une trace lisible.

## Propositions d'amélioration

Aucune modification de spécification n'est proposée.

Une amélioration pédagogique possible, sans changer la roadmap, serait d'ajouter plus tard un exercice comparatif entre :

- boucle contrôlée côté application ;
- boucle gérée par un framework agentique ;
- boucle multi-agent avec délégation.
