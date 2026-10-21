# Protocole d’évaluation du retrieval

Le corpus contient huit documents fictifs : sept team-a et un team-b. Huit questions positives sont annotées par document; deux questions hors corpus testent l’abstention. Les quatre modes sont exécutés sur les mêmes sources.

## Métriques

Dédupliquer les documents retrouvés en conservant leur première occurrence. Recall@k = documents pertinents dans les k premiers / tous les documents pertinents. MRR@k = inverse du rang du premier pertinent dans les k premiers, sinon zéro. nDCG@k utilise des jugements binaires et un gain 1/log2(rang+1), normalisé par le meilleur classement possible.

Un cas sans pertinent connu ne passe pas par une division par zéro : il appartient aux tests d’abstention. Un document pertinent pour une question doit appartenir à son périmètre autorisé. Le marqueur privé team-b sert aux contrôles d’isolation, pas à une information à produire pour team-a.

## Lecture des résultats

Les questions q1 à q7 sont proches du vocabulaire des documents. q8 paraphrase le rejeu d’un paiement sans les termes les plus évidents; conserver son échec pour montrer les limites lexicales. Les collisions de hashbow peuvent donner des candidats accidentels, sans constituer une preuve de compréhension.

Les moyennes du minuscule jeu de développement n’estiment pas une performance de production. Ajouter un jeu réservé avec plusieurs pertinents, questions multi-passages, identifiants rares, paraphrases et cas hors corpus. Une nouvelle annotation ne doit pas simplement aligner les qrels sur la sortie observée.

Le rapport trace corpus, qrels et empreinte d’encodeur. Il n’évalue pas une génération LLM, une factualité générale, une charge concurrente ou la qualité d’un modèle neuronal. Les adaptateurs optionnels exigent une campagne séparée.
