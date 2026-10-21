# S8 J3 — Observabilité, SLI et diagnostic


## 1. Passer du statut à l’explication
Un processus peut être disponible alors que ses réponses sont inutiles ou que les demandes attendent une revue humaine. L’observabilité doit permettre de distinguer erreurs techniques, échecs de qualité et attente métier. Les semaines 4 et 5 introduisaient l’instrumentation; ce jour se concentre sur le choix des signaux, les dénominateurs et le diagnostic d’un système IA.

La fonction telemetry produit des journaux JSON corrélés et des compteurs par statut. C’est un format pédagogique, sans SDK OpenTelemetry, collecteur ni export OTLP. Chaque essai possède une trace avec un span racine simulé. Un identifiant seul n’implémente pas une propagation distribuée : pour une intégration réelle, les services doivent extraire et transmettre un contexte cohérent.

## 2. Définir ce que mesure chaque signal
Une métrique décrit une population agrégée; un journal décrit un événement; une trace représente un parcours et ses opérations. Dans ce lab, l’erreur technique correspond à status différent de ok. Un succès technique ne garantit pas une réponse correcte : c09 est techniquement traité mais échoue à l’évaluation critique.

Le compteur candidat observe 35 ok et un timeout. Cette population de 36 tentatives diffère des douze cas de qualité de J1. Les dénominateurs ne doivent pas être mélangés. Une alerte qualité peut provenir de contrôles annotés, tandis qu’une alerte de disponibilité s’appuie sur les réponses techniques. Leur corrélation aide à enquêter; elle ne prouve pas une cause unique.

## 3. Écrire un SLI sans ambiguïté
Définir la population éligible, l’événement bon, la fenêtre temporelle et le traitement des erreurs. Exemple pédagogique : parmi toutes les tentatives éligibles de la fenêtre, est bonne une tentative techniquement réussie terminée en moins de 1000 ms. Un timeout reste dans le dénominateur et est mauvais.

Un SLO de 99 % sur une fenêtre de trente jours n’est pas vérifiable avec ces trente-six observations synthétiques sans dates réelles. Le lab calcule seulement un taux sur le lot. Si 35/36 réussissent, le SLI du lot vaut environ 97,22 %. Ce nombre ne mesure pas le service en production. Un budget d’erreur n’est pas un budget financier; nommer clairement les deux.

## 4. Isoler le temps humain
Le champ duration_ms décrit le traitement automatisé; human_wait_ms décrit une attente séparée. Le p95 d’attente humaine vaut 12000 ms dans les fixtures. Les additionner sans définir le point de départ et la population pourrait confondre performance technique et délai métier.

Pour un processus réel, conserver des événements de cycle de vie et des horodatages cohérents. Mesurer l’âge de la plus ancienne demande en attente, les expirations et le temps total jusqu’à la décision. Une API peut répondre vite avec 202 et accumuler une file inexploitable. C’est la continuité directe des états durables de S7.

## 5. Minimisation et cardinalité
La fonction exporte une liste autorisée de champs : trace_id, span_id, parent_span_id, version, status et duration_ms. Elle ne copie ni prompt, ni texte du ticket, ni credential. Les identifiants de trace servent à la corrélation des événements; ils ne deviennent pas des labels de métriques par requête.

Le nombre de séries augmente avec les combinaisons de labels. Utiliser une dimension status bornée est plus maîtrisable qu’un identifiant utilisateur ou un texte libre. Une allowlist réduit la surface de collecte; elle ne remplace pas la vérification des valeurs autorisées, des droits de consultation et de la rétention. Les fixtures ne contiennent aucune donnée client réelle.

## 6. Diagnostiquer puis agir
Un runbook part du symptôme, vérifie population et changements de configuration, puis détaille la recherche par identifiant de trace. Une réponse 200 avec qualité mauvaise appelle l’analyse du corpus, du prompt ou des outils; un timeout appelle d’abord l’analyse des dépendances et de la charge. Une alerte doit conduire à une action documentée, pas à une collection infinie de logs.

## À retenir
Le bon signal correspond à une question opérationnelle. Les compteurs techniques, l’évaluation de qualité et l’attente humaine décrivent des populations différentes.
