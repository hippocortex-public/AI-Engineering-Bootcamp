# S9 J7 — Projet RAG : preuves, abstention et évaluation


## 1. Un pipeline complet de connaissances
Le projet reçoit une question, sélectionne les passages autorisés, fusionne les classements, reclassifie les candidats, applique un seuil explicite et assemble un contexte borné. La réponse locale reproduit les extraits avec leurs références. Le projet démontre le pipeline de retrieval et le contrat d’un RAG; il ne contacte pas de modèle génératif.

Cette distinction est volontaire : l’encodage hashbow, BM25, RRF, SQLite, les filtres et les métriques s’exécutent réellement. La synthèse par LLM reste un raccord à construire après évaluation du retrieval. Le port neuronal optionnel ne transforme pas la réponse extractive en une génération.

## 2. Une citation vérifiable
Chaque référence contient chunk_id, doc_id, version, start, end, text et source. citation_valid charge le chunk courant dans le tenant et compare les champs. Une citation inventée, modifiée ou liée à une ancienne version échoue. La réponse par défaut ne produit que des extraits exacts, ce qui rend le contrat facile à inspecter.

Une référence valide ne prouve pas que le document est juste. Avec un LLM, elle ne prouverait pas non plus que toutes ses affirmations sont soutenues par le passage cité. Il faudrait évaluer fidélité, couverture des affirmations, contradictions et utilité. Ne pas nommer « zéro hallucination » un simple test d’identifiants de sources.

## 3. Abstention et limites lexicales
Le moteur peut s’abstenir si aucun passage ne satisfait le seuil de couverture ou si le budget ne permet pas d’en conserver. Deux questions hors corpus servent de cas d’abstention. Une absence de réponse peut aussi être un faux négatif : q8 paraphrase une question connue mais utilise des mots éloignés de la baseline.

Un système réel doit distinguer absence d’information, retrieval raté, autorisation insuffisante et budget trop faible. La réponse locale regroupe ces situations sous abstain et explique sa portée. Améliorer ce diagnostic constitue une extension, pas une garantie cachée. Aucun document team-b n’est ajouté pour remplir un contexte team-a trop pauvre.

## 4. Mesures de retrieval
Le jeu contient huit requêtes positives avec qrels au niveau document. Recall@k est la fraction des documents pertinents retrouvés dans les k premiers documents distincts. MRR@k est l’inverse du rang du premier pertinent dans cette coupure, sinon zéro. nDCG@k compare le gain actualisé observé au meilleur classement possible; les jugements sont binaires dans ce lab.

Les requêtes sans document pertinent ne sont pas forcées dans une formule au dénominateur nul. Elles alimentent le contrôle d’abstention. Le rapport conserve les résultats par requête, les moyennes, l’empreinte du corpus, des qrels et de l’encodeur. Les questions constituent un jeu de développement minuscule, sans échantillon de validation réservé.

## 5. Comparer les variantes sans inventer un gain
Les modes lexical, vector, hybrid et reranked sont évalués sur les mêmes questions. Un résultat identique ou une dégradation doit rester dans le rapport. Le cas q8 rend visible que les canaux lexicaux ne démontrent pas une capacité sémantique. Ajouter un modèle appris réclame une nouvelle mesure, pas une réutilisation des scores de hashbow.

La semaine 8 fournissait des principes de décision et de traçabilité. Ce projet les applique à la récupération de connaissances avec des métriques spécifiques, sans réécrire les modules partagés. Une intégration réelle peut transmettre les rapports à votre dispositif de supervision après alignement explicite des contrats.

## 6. Revue d’architecture
Présenter ingestion atomique, index exact, autorisations préalables, compatibilité d’encodeur, mémoire séparée et citations. Expliquer ensuite les limites : tenant seul, un processus SQLite, pas d’ANN, pas de génération, corpus fictif et pas de campagne de pertinence neuronale.

Pour aller plus loin, choisir une amélioration dont le besoin est mesuré : encodeur sémantique pour les paraphrases, pgvector pour une expérimentation de stockage, reranker appris pour les candidats ambigus ou générateur évalué pour la synthèse. Chaque ajout doit conserver suppression, isolation et provenance.

## À retenir
Un RAG exploitable relie recherche, autorisation, références et mesure de qualité. Une bonne démonstration expose aussi les questions qu’elle ne sait pas traiter.
