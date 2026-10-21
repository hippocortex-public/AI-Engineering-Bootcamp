# Architecture du système de connaissances S9

## Décision

Séparer document source, projection de chunks, encodeur, store, stratégies de ranking, mémoire et réponse. Le module obligatoire utilise la bibliothèque standard et un scan exact pour permettre l’inspection des invariants sans infrastructure supplémentaire.

| Composant | Contrat | Limite |
|---|---|---|
| chunk_document | Paragraphes/fenêtres, provenance et offsets exacts | Mots d’espace, pas tokens LLM |
| HashEmbedding | Projection signée déterministe normalisée | Lexical, collisions, pas de synonymie apprise |
| Store SQLite | Métadonnées, vecteurs, versions et transactions | Un processus, scan exact, pas ANN |
| BM25 + RRF | Classements puis fusion des rangs | Complémentarité à mesurer |
| rerank + context_pack | Couverture lexicale et passages entiers | Pas CrossEncoder, budget de mots |
| memory | Portée tenant/user/session et TTL | Expiration logique, sans purge automatique |
| answer | Extraits cités ou abstention | Aucune synthèse générative |

## Invariants

Le filtre tenant s’applique avant scoring et top-k. L’encodeur et sa dimension doivent correspondre à l’index. Une version documentaire ne change pas de contenu. Le remplacement d’un document et de ses chunks est atomique localement. Une citation correspond à un chunk courant du périmètre. La mémoire ne devient pas une preuve documentaire. Une source modifiée masque ses notes dérivées; sa suppression les retire du store.

## Frontières de confiance

Tenant, utilisateur et session sont des paramètres de laboratoire; un vrai service doit les résoudre à partir d’une identité autorisée. Le store n’ajoute ni authentification ni RBAC par document. Les fichiers du corpus sont des sources fictives locales, pas des instructions exécutées. Le moteur ne dispose d’aucun outil d’action externe.

Une citation valide confirme l’existence du passage courant, pas sa vérité. Une empreinte locale permet une comparaison de contenu; elle n’atteste pas l’origine d’une mesure ni l’identité d’un éditeur. La réponse par défaut reproduit les passages au lieu de produire des affirmations supplémentaires.

## Migration

Pour changer d’encodeur : créer un index distinct, réencoder toutes les sources, comparer un jeu de questions réservé puis basculer le pointeur du service. Une dimension identique n’établit pas un espace commun. Pour passer à pgvector : mesurer d’abord une recherche exacte, puis les compromis d’un index ANN avec les filtres réels.

## Raccord à un générateur

Construire le contexte à partir des passages autorisés, conserver leur identifiant et séparer instructions de l’application et contenu documentaire non fiable. Compter le budget avec le tokenizer du modèle en incluant question, wrappers et réserve de sortie. Valider les identifiants de citations mais évaluer aussi l’appui réel des affirmations. Les permissions d’outils restent applicatives.

Cette archive ne fournit pas de client LLM de génération et n’en annonce aucune validation. Le laboratoire extractif permet de tester retrieval, isolation et provenance avant de choisir ce raccord.

## Propositions d’amélioration

Titres rattachés aux paragraphes, modèle sémantique évalué, reranker appris, index ANN mesuré, purge des notes expirées, droits plus fins et génération évaluée. Ces changements demandent leurs propres tests et ne modifient aucune spécification gelée.
