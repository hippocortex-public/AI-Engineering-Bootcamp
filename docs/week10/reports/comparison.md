# Rapport NLP — Semaine 10

Corpus fictif; entraînements scikit-learn réellement exécutés. Aucun LLM ni LoRA exécuté.

## Classification

| Mesure test | Baseline | Tête adaptée |
|---|---|---|
| count | 12 | 12 |
| accuracy_argmax | 1.0 | 1.0 |
| macro_f1_argmax | 1.0 | 1.0 |
| coverage | 1.0 | 1.0 |
| selective_accuracy | 1.0 | 1.0 |
| threshold | 0.34 | 0.34 |

Epochs retenus par validation : 1. Vocabulaire inchangé : True. Poids modifiés : True.

L’adaptation change réellement les poids mais ne démontre pas de gain de F1 sur ce test facile. Aucun réglage n’a été choisi sur le test. Les résultats hors distribution sont inspectables avec la démo J1.

## Extraction et NER

16/16 valeurs et 16/16 statuts corrects. Les champs ambigus restent null avec preuves conservées.

NER : 12 spans exacts sur des noms connus, F1=1.0. Ce résultat ne prouve pas le rappel sur de nouvelles entités ni un masquage exhaustif.

## Projection spécialisée

| Mode | Dimension | Precision@3 | Recall@3 | MRR@3 |
|---|---|---|---|---|
| tfidf | 441 | 0.9167 | 0.2292 | 1.0000 |
| supervised_nca | 8 | 1.0000 | 0.2500 | 1.0000 |

La pertinence est un proxy de même catégorie. Douze documents train sont pertinents par classe : le Recall@3 maximal vaut 0,25. Ce protocole ne mesure pas une pertinence sémantique humaine.

## Limites

72 tickets courts et fictifs, quatre exemples intégrés, labels simples. Le résumé est extractif et son proxy lexical n’évalue pas les omissions critiques. Le modèle reste non calibré pour le hors distribution. Les artefacts JSON gardent une empreinte locale, sans authentification d’auteur. Aucun service de production n’est déployé.
