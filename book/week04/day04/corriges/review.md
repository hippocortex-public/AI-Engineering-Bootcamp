# Review formateur

## Objectifs validés

L'apprenant doit être capable d'expliquer et de coder :

- un record mémoire ;
- une requête mémoire ;
- la séparation namespace/visibility/kind ;
- l'expiration TTL ;
- la redaction PII ;
- la restauration depuis snapshot ;
- l'audit des écritures.

## Points d'attention

### 1. Ne pas confondre mémoire et historique

Une erreur fréquente consiste à stocker chaque message comme mémoire durable. Le formateur doit insister : toute conversation n'est pas une mémoire.

### 2. Ne pas confondre recherche et injection

Retrouver une mémoire ne signifie pas qu'elle doit être injectée dans le prompt. Il faut encore filtrer, ranker, compacter et respecter le budget.

### 3. Ne pas créer de mémoire globale

Le namespace est obligatoire. Toute mémoire sans namespace est une dette de sécurité.

### 4. Éviter la persistance prématurée

Le lab utilise l'in-memory pour enseigner le contrat. La persistance arrive plus tard, mais le contrat doit déjà permettre le remplacement.

## Checklist de correction

- [ ] Le code s'exécute sans dépendance externe.
- [ ] Les tests passent.
- [ ] Les records ont un namespace.
- [ ] La visibilité est appliquée.
- [ ] Les records expirés sont exclus.
- [ ] `forget_namespace` ne supprime pas les autres namespaces.
- [ ] Le snapshot est restaurable.
- [ ] Les événements sont audités.
- [ ] Le code reste compréhensible pour un AI Engineer junior/intermédiaire.

## Propositions d'amélioration

- Ajouter une interface abstraite `MemoryBackend`.
- Ajouter une stratégie de compaction.
- Ajouter un backend SQLite.
- Ajouter une étape de validation humaine avant promotion de mémoire sensible.
- Ajouter un score hybride lexical + vectoriel lors de la semaine Knowledge Systems.
