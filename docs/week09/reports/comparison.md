# Rapport de retrieval — Semaine 9

Corpus fictif, calculs réellement exécutés; aucun modèle neuronal ou génératif interrogé.

| Mode | Recall@3 | MRR@3 | nDCG@3 |
|---|---|---|---|
| lexical | 0.8750 | 0.8750 | 0.8750 |
| vector | 1.0000 | 0.9167 | 0.9375 |
| hybrid | 1.0000 | 0.9167 | 0.9375 |
| reranked | 1.0000 | 0.9167 | 0.9375 |

## Cas de paraphrase q8

- lexical : documents [], Recall@3=0.0.
- vector : documents ['otel-traces', 'kafka-rate', 'kafka-replay'], Recall@3=1.0.
- hybrid : documents ['otel-traces', 'kafka-rate', 'kafka-replay'], Recall@3=1.0.
- reranked : documents ['otel-traces', 'kafka-rate', 'kafka-replay'], Recall@3=1.0.

Sur q8, hashbow retrouve le document pertinent au rang 3 grâce à des similarités de projection accidentelles, mais le premier résultat est un autre sujet. La réponse extractive s’abstient : aucun passage ne satisfait la couverture lexicale. Ce gain de Recall@3 ne prouve donc aucune compréhension des synonymes. Ne pas supprimer ce cas pour améliorer la moyenne. Les deux questions hors corpus sont conservées dans retrieval.json avec leur statut d’abstention.

## Provenance

Corpus : `308e049896949fdf0fbfd37e849e54c4d9432731c89bc8068b26c0243ccad06e`.

Qrels : `d2348c5fc3ce1334dc8b54d2241d04cd5050bb93e8f367de5987e8063ec6713a`.

Encodeur : `hashbow-sha256-v1:dim=128:tokens=nfkd-stop-v1`.

Le jeu contient huit questions positives et deux questions hors corpus. Il est réservé à la démonstration et au développement, sans validation indépendante de production. Une citation vérifiée n’est pas une preuve de vérité générale.
